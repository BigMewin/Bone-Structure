from __future__ import print_function
import numpy as np
import os
import radiomics
from radiomics import featureextractor
import gc
import psutil

# Set the parameters for feature extraction
settings = {
    'label': 255,
    'binWidth': 1,
    'force2D': 0,
    'distances': [1, 2, 3, 4, 5],
    'weightingNorm': 'no_weighting'
}

# Initialize the feature extractor
extractor = featureextractor.RadiomicsFeatureExtractor(**settings)
extractor.disableAllFeatures()
extractor.enableFeatureClassByName('glcm')
extractor.enableFeatureClassByName('glrlm')

# Directory for saving results
base_save_dir = 'bone4_text_5mm'

os.makedirs(base_save_dir, exist_ok=True)

# Define the range of thresholds for i and j
#i_values = [400]
#j_values = [1000]
i_values = range(-800, 401, 100)
j_values = range(500, 1001, 100)

# Loop through each threshold combination
for i_val in i_values:
    for j_val in j_values:
        if i_val == -800 and j_val == 1000:
            print('skip -800_1000')
            continue
        threshold = f'{i_val}_{j_val}'
        threshold_save_dir = os.path.join(base_save_dir, f'{threshold}')
        os.makedirs(threshold_save_dir, exist_ok=True)

        feature_names = None
        threshold_features = []  # Initialize list to store feature values for each threshold

        # Process each ROI individually
        for roi_num in range(1, 71):
        #for roi_num in range(1, 26):
            roi_file = f'UHR_ROI_{roi_num}_threshold_{threshold}.nii'
            imagePath = os.path.join('D:', 'd_users', 'Yuchen', 'HRPQCT_UHR_NR', '071_F221272_HRPQCT', 'bone4_ROI_circle_5mm', roi_file)
            maskPath = os.path.join('D:', 'd_users', 'Yuchen', 'HRPQCT_UHR_NR', '071_F221272_HRPQCT', 'bone4_ROI_circle_5mm', f'Single_Circle_thresholdnew1_{threshold}.nii')

            # Check if the feature file already exists
            roi_feature_file = os.path.join(threshold_save_dir, f'features_{roi_file.split(".")[0]}.npy')

            if os.path.exists(roi_feature_file):
                # Load the existing features if they already exist
                print(f"Loading features for ROI_{roi_num} for threshold {threshold}")
                feature_values = np.load(roi_feature_file)
            else:
                # If either the image or mask file does not exist, skip
                if not os.path.exists(imagePath) or not os.path.exists(maskPath):
                    print(f"Skipping ROI_{roi_num} for threshold {threshold} because the file does not exist.")
                    continue

                print(f"Processing ROI_{roi_num} for threshold {threshold}")

                try:
                    result = extractor.execute(imagePath, maskPath)
                except Exception as e:
                    print(f"Error processing {roi_file}: {e}")
                    continue

                glcm_features = {k: v for k, v in result.items() if 'glcm' in k}
                glrlm_features = {k: v for k, v in result.items() if 'glrlm' in k}

                combined_features = {**glcm_features, **glrlm_features}
                feature_values = np.array(list(combined_features.values()))

                np.save(roi_feature_file, feature_values)  # Save features for each ROI

                if feature_names is None:
                    feature_names = list(combined_features.keys())

            threshold_features.append(feature_values)  # Append features to the threshold-specific list

            #del feature_values, result, glcm_features, glrlm_features
            gc.collect()

        # After processing all ROIs, save the combined feature matrix
        features_matrix = np.array(threshold_features)
        np.save(os.path.join(threshold_save_dir, 'features_matrix.npy'), features_matrix)

        # Save feature names (once for each threshold)
        if feature_names:
            np.save(os.path.join(threshold_save_dir, 'feature_names.npy'), np.array(feature_names))

# Display the completion message
print("Processing complete.")
