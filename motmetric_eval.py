# import required packages
import motmetrics as mm
import numpy as np

def read_txt_file(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith("#") or not line.strip():
                continue
            parts = line.strip().split(',')
            frame_id = int(parts[0])
            object_id = int(parts[1])
            x = float(parts[2])
            y = float(parts[3])
            width = float(parts[4])
            height = float(parts[5])
            data.append((frame_id, object_id, x, y, width, height))
    return data

def load_data(accumulator, gt_data, pred_data):
    frame_ids = set([d[0] for d in gt_data + pred_data])
    
    for frame_id in frame_ids:
        gt_frame_data = [d for d in gt_data if d[0] == frame_id]
        pred_frame_data = [d for d in pred_data if d[0] == frame_id]

        gt_ids = [d[1] for d in gt_frame_data]
        gt_dets = [(d[2], d[3], d[4], d[5]) for d in gt_frame_data]

        pred_ids = [d[1] for d in pred_frame_data]
        pred_dets = [(d[2], d[3], d[4], d[5]) for d in pred_frame_data]

        dists = mm.distances.iou_matrix(gt_dets, pred_dets, max_iou=0.5)
        accumulator.update(gt_ids, pred_ids, dists)


# Main code
gt_file_path = 'gt_mot/236_1_gt.txt'
pred_file_path = 'FairMOT_ROOT/demos/results.txt'

ground_truth = read_txt_file(gt_file_path)
predictions = read_txt_file(pred_file_path)

# Create an accumulator
acc = mm.MOTAccumulator(auto_id=True)

# Load the data into the accumulator
load_data(acc, ground_truth, predictions)

# Compute metrics
mh = mm.metrics.create()
summary = mh.compute(acc, metrics=mm.metrics.motchallenge_metrics, name='acc')

# Display results
str_summary = mm.io.render_summary(
    summary, 
    formatters=mh.formatters,
    namemap=mm.io.motchallenge_metric_names
)
print(str_summary)