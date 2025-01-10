
import json
import csv

# Part 1: Conversion of tracker_wise JSON to frame_wise JSON
def convert_tracker_to_frame_wise(input_file, output_file):
    with open(input_file, 'r') as f:
        tracker_data = json.load(f)

    annotations = tracker_data["maker_response"]["video2d"]["data"]["annotations"]
    riders = tracker_data['rider_info']
    frame_wise = {"export_data": {"annotations": {"frames": {}}}}
    no_of_annotations = 0
    for tracker in annotations:
        tracker_id = tracker["_id"]
        label = tracker['label']
        type = tracker['type']
        no_of_annotations += len(tracker['frames'])
        for frame_name, annotation in tracker["frames"].items():
            frame_info={}
            frame_info['_id'] = annotation['_id']
            frame_info['label']= label
            frame_info['type']= type
            for loc_key, loc_info in annotation['points']['p1'].items():
                frame_info['point_' + loc_key]= loc_info

            for a_key, a_value in annotation['attributes'].items():
                frame_info[a_key]= a_value['value']
  
           
            rider_id= riders[frame_name]['rider_id']
            frame_info['rider_id']=rider_id
            frame_info['tracker_id']= tracker_id

            if frame_name not in frame_wise["export_data"]["annotations"]["frames"]:
                frame_wise["export_data"]["annotations"]["frames"][frame_name] = []
                
            frame_wise["export_data"]["annotations"]["frames"][frame_name].append(frame_info)

    frame_wise['export_data']['number of annotations'] = no_of_annotations
    with open(output_file, 'w') as f:
        json.dump(frame_wise, f, indent=4)


# Part 2: Creating a CSV file with frame_id, tracking_id, and label
def create_csv(input_file, output_csv):
    with open(input_file, 'r') as f:
        tracker_data = json.load(f)

    annotations = tracker_data["maker_response"]["video2d"]["data"]["annotations"]

    with open(output_csv, 'w', newline='') as csvfile:
        fieldnames = ["frame_id", "tracking_id", "label"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for tracker in annotations:
            tracker_id = tracker["_id"]
            for frame_id, annotation in tracker["frames"].items():
                writer.writerow({
                    "frame_id": frame_id,
                    "tracking_id": tracker_id,
                    "label": annotation.get("label", "")
                })

print("Frame-wise JSON conversion completed and saved to 'frame_wise.json'")

input_json = "input.json"
output_json = "frame_wise.json"
output_csv = "frame_annotations.csv"

convert_tracker_to_frame_wise(input_json, output_json)
create_csv(input_json, output_csv)
