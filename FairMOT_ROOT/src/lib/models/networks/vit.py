import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from einops import rearrange, repeat
import numpy as np
import os
from tqdm import tqdm
from collections import OrderedDict



class Residual(nn.Module):
    def __init__(self, fn):
        super().__init__()
        self.fn = fn
    def forward(self, x, **kwargs):
        return self.fn(x, **kwargs) + x

class PreNorm(nn.Module):
    def __init__(self, dim, fn):
        super().__init__()
        self.norm = nn.LayerNorm(dim)
        self.fn = fn
    def forward(self, x, **kwargs):
        return self.fn(self.norm(x), **kwargs)

class FeedForward(nn.Module):
    def __init__(self, dim, hidden_dim, dropout=0.):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(dim, hidden_dim),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, dim),
            nn.Dropout(dropout)
        )
    def forward(self, x):
        return self.net(x)

class Attention(nn.Module):
    def __init__(self, dim, heads=8, dim_head=64, dropout=0.):
        super().__init__()
        inner_dim = dim_head * heads
        project_out = not (heads == 1 and dim_head == dim)

        self.heads = heads
        self.scale = dim_head ** -0.5

        self.to_qkv = nn.Linear(dim, inner_dim * 3, bias=False)
        self.to_out = nn.Sequential(
            nn.Linear(inner_dim, dim),
            nn.Dropout(dropout)
        ) if project_out else nn.Identity()

    def forward(self, x, mask=None):
        b, n, _, h = *x.shape, self.heads
        qkv = self.to_qkv(x).chunk(3, dim=-1)
        q, k, v = map(lambda t: rearrange(t, 'b n (h d) -> b h n d', h=h), qkv)

        dots = torch.einsum('b h i d, b h j d -> b h i j', q, k) * self.scale
        mask_value = -torch.finfo(dots.dtype).max

        if mask is not None:
            mask = F.pad(mask.flatten(1), (1, 0), value=True)
            assert mask.shape[-1] == dots.shape[-1], 'mask has incorrect dimensions'
            mask = rearrange(mask, 'b i -> b () i ()') * rearrange(mask, 'b j -> b () () j')
            dots.masked_fill_(~mask, mask_value)
            del mask

        attn = dots.softmax(dim=-1)

        out = torch.einsum('b h i j, b h j d -> b h i d', attn, v)
        out = rearrange(out, 'b h n d -> b n (h d)')
        out = self.to_out(out)
        return out

class Transformer(nn.Module):
    def __init__(self, dim, depth, heads, dim_head, mlp_dim, dropout=0.):
        super().__init__()
        self.layers = nn.ModuleList([])
        for _ in range(depth):
            self.layers.append(nn.ModuleList([
                Residual(PreNorm(dim, Attention(dim, heads=heads, dim_head=dim_head, dropout=dropout))),
                Residual(PreNorm(dim, FeedForward(dim, mlp_dim, dropout=dropout)))
            ]))
    def forward(self, x, mask=None):
        for attn, ff in self.layers:
            x = attn(x, mask=mask)
            x = ff(x)
        return x

class ViT_BACKBONE(nn.Module):
    def __init__(self, *, width, height, patch_size, dim, depth, heads, mlp_dim, channels=3, dim_head=64, dropout=0., emb_dropout=0.):
        super().__init__()
        assert width % patch_size == 0 and height % patch_size == 0, 'Image dimensions must be divisible by the patch size.'
        self.patch_size = patch_size
        num_patches = (width // patch_size) * (height // patch_size)
        patch_dim = channels * patch_size ** 2

        self.feat_width = width // patch_size
        self.feat_height = height // patch_size

        self.to_patch_embedding = nn.Linear(patch_dim, dim)

        self.pos_embedding = nn.Parameter(torch.randn(1, num_patches, dim))
        self.dropout = nn.Dropout(emb_dropout)
        self.transformer = Transformer(dim, depth, heads, dim_head, mlp_dim, dropout)

        # Projection layer to match the dimension for FairMOT heads
        self.proj_layer = nn.Conv2d(dim, 256, kernel_size=1)

        # FairMOT heads
        self.hm_head = nn.Sequential(
            nn.Conv2d(256, 256, kernel_size=3, padding=1),
            nn.Conv2d(256, 1, kernel_size=1)
        )
        self.wh_head = nn.Sequential(
            nn.Conv2d(256, 256, kernel_size=3, padding=1),
            nn.Conv2d(256, 4, kernel_size=1)
        )
        self.reid_head = nn.Conv2d(256, 128, kernel_size=1)

        self.reg_head = nn.Sequential(
            nn.Conv2d(256, 256, kernel_size=3, padding=1),
            nn.Conv2d(256, 2, kernel_size=1)
        )

    def forward(self, img, mask=None):
        p = self.patch_size

        # Rearrange image into patches
        x = rearrange(img, 'b c (h p1) (w p2) -> b (h w) (p1 p2 c)', p1=p, p2=p)

        x = self.to_patch_embedding(x)
        b, n, _ = x.shape

        # Add positional embedding
        x += self.pos_embedding[:, :n]
        x = self.dropout(x)

        # Apply transformer
        x = self.transformer(x, mask)
        print(f"Shape after Transformer output: {x.shape}")  # Debugging print
        print('=' * 80)
        #Reshape transformer output back to 2D feature map
        x = x.reshape(b, self.feat_height, self.feat_width, -1)
        print(f"Feature map shape: {x.shape}")  # Debugging print
        print('=' * 80)
        x = x.permute(0, 3, 1, 2)  

        x = F.interpolate(x, size=(152, 272), mode='bilinear', align_corners=False)
        
        print(f"Upsample shape: {x.shape}")  # Debugging print


        # Project to 256 channels
        x = self.proj_layer(x)
        print(f"Shape after projection layer: {x.shape}")  # Debugging print



        #Apply FairMOT heads
        hm = self.hm_head(x)
        wh = self.wh_head(x)
        reid = self.reid_head(x)
        reg = self.reg_head(x)

        
        return [{
            'hm': hm,
            'wh': wh,
            'id': reid,
            'reg': reg
        }]
