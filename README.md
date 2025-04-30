# Bone Metric Analysis Pipeline

This MATLAB pipeline provides a complete workflow for bone segmentation, ROI extraction, and morphometric analysis of HRPQCT and PCCT scans. It registers two volumes, extracts ROIs, and calculates standard bone metrics.

## Prerequisites

- MATLAB with Image Processing Toolbox
- NIfTI toolbox (functions: `load_nii`, `save_nii`, `make_nii`)
- TrabecularMetricPackage (for bone metric calculations)

## Pipeline Overview

1. Load and segment the HRPQCT scan
2. Identify central points for ROIs
3. Transform coordinates to match the PCCT scan using the registration matrix
4. Extract ROIs from both volumes
5. Apply circular masks for consistent analysis
6. Calculate bone metrics:
   - BV/TV (Bone Volume Fraction)
   - Tb.Th (Trabecular Thickness)
   - Tb.Sp (Trabecular Separation)
   - Tb.N (Trabecular Number)

## Usage Instructions

### Step 1: Update File Paths

Update the following file paths to match your data:

```matlab
% HRPQCT scan path
HRPQCT_scan = load_nii('00000389 - PF_upper_half.nii');

% PCCT scan path
PCCT_scan = load_nii('FEMUR2_0CM_UHR_S2_HD_PF_lower_1_8_new.nii');

% Output directories
output_dir = 'bone1_ROI_circle_3mm_PF';  % For storing PCCT ROIs
roi_folder = 'bone1_hrpq_3mm_PF';        % For storing HRPQCT ROIs
saveDir = 'saved_hrpq_bone1_3mm_PF';     % For storing metric results
```

### Step 2: Adjust Registration Parameters

Update the transformation matrix and translation vector based on your MITK registration results:

```matlab
% Transformation matrix (3x3 rotation matrix)
Transformation = [0.995288 0.0174464 0.0953764;
                  0.0148635 -0.999505 0.0277252;
                  0.0958129 -0.0261769 -0.995055];

% Center of rotation
Center = [-38.2106, -48.8331, 25.5243]';

% Translation vector
Translation = [-35.5, -25.79, 12.6]';
```

### Step 3: Adjust Segmentation Parameters

Modify the segmentation parameters for your bone type:

```matlab
% Segmentation threshold for HRPQCT
bone_threshold = 3000;

% Morphological operation parameters
se = strel('disk', 10);  % Adjust the disk size for gap closing
```

### Step 4: Modify ROI Parameters

Adjust ROI size and voxel dimensions:

```matlab
% ROI size in millimeters
radius_mm = 3;
edge_length_mm = 6;

% Pixel/voxel size in mm
pixel_size_mm = 0.0607;           % For HRPQCT
voxel_size_mm = PCCT_Dim(1);      % For PCCT
```

### Step 5: Adjust Thresholding Parameters

Modify PCCT segmentation thresholds:

```matlab
% Define step size for threshold ranges
step_size = 100;

% Generate threshold ranges
lower_bounds = -800:step_size:400;
upper_bounds = 500:step_size:1000;
```

### Step 6: Modify Concentric Circle Parameters

Set concentric circle sizes and intensities:

```matlab
% Define radii in mm
radii_mm = [3, 3.607, 4.214];

% Intensities for the concentric circles
intensities = [3, 2, 1];
```

## Running the Pipeline

The code is designed to run sequentially. The main steps include:

1. Segmentation of HRPQCT scan
2. Central point detection for ROIs
3. Coordinate transformation between HRPQCT and PCCT
4. ROI extraction from both scans
5. Circular mask application for consistency
6. Metric calculation for bone structure

### Output

- Individual ROI NIfTI files saved in specified folders
- Text files with metrics for each ROI
- A summary CSV file: `morphor_bone1_PF.csv`

## Output Metrics

- **BV/TV**: Bone Volume Fraction
- **Tb.Th**: Trabecular Thickness
- **Tb.Sp**: Trabecular Separation
- **Tb.N**: Trabecular Number

## Tips for Registration in MITK

1. Load both volumes in MITK.
2. Use the Manual Registration tool for initial alignment.
3. Use Rigid Registration for fine adjustments.
4. Export the transformation matrix.
5. Convert the matrix to the format:

   [R | t]

   where `R` is a 3x3 rotation matrix and `t` is a 3x1 translation vector.

## Troubleshooting

- **Misaligned ROIs**: Check transformation matrix and translation vector
- **Poor segmentation**: Adjust the `bone_threshold`
- **Incorrect metrics**: Verify mask parameters
- **Errors**: Ensure required packages are in the MATLAB path

## Example Workflow

1. Register HRPQCT and PCCT scans using MITK
2. Record the transformation matrix and translation vector
3. Update this information in the MATLAB code
4. Adjust parameters as needed
5. Run the script
6. Review the output metrics in the resulting CSV file
7. 




# Texture Feature Extraction Pipeline

This script (`texture_feat.py`) extracts GLCM and GLRLM texture features from a series of bone ROI NIfTI files using PyRadiomics. It loops through thresholded masks and corresponding images, computes features for each ROI, and saves the results for downstream analysis.

---

## Requirements

- Python 3.7+
- `pyradiomics`
- `numpy`
- `psutil`

You can install dependencies with:

```bash
pip install pyradiomics numpy psutil
```

---

## How to Run

Run the script using Python:

```bash
python texture_feat.py
```

The script will process all ROI files across multiple thresholds and save the extracted features to disk.

---

## Directory Structure

You should organize your data like this:

```
D:/d_users/Yuchen/HRPQCT_UHR_NR/071_F221272_HRPQCT/
│
├── bone4_ROI_circle_5mm/
│   ├── UHR_ROI_1_threshold_...nii
│   ├── Single_Circle_thresholdnew1_...nii
│   └── ...
```

The script saves results under:

```
./bone4_text_5mm/
├── {threshold}/
│   ├── features_matrix.npy
│   ├── feature_names.npy
│   ├── features_UHR_ROI_1_....npy
│   └── ...
```

---

## Configurable Parameters

All parameters are set at the top of the script. You can edit them as needed:

### Feature Settings

```python
settings = {
    'label': 255,
    'binWidth': 1,
    'force2D': 0,
    'distances': [1, 2, 3, 4, 5],
    'weightingNorm': 'no_weighting'
}
```

You can modify which features to extract by changing:

```python
extractor.enableFeatureClassByName('glcm')
extractor.enableFeatureClassByName('glrlm')
```

You can also add `'firstorder'`, `'shape'`, `'ngtdm'`, etc.

---

### Thresholds

Change the threshold combinations here:

```python
i_values = range(-800, 401, 100)
j_values = range(500, 1001, 100)
```

To test only a few specific thresholds:

```python
i_values = [400]
j_values = [1000]
```

---

### Input Paths

The NIfTI image and mask paths are set here:

```python
imagePath = os.path.join('D:', 'd_users', 'Yuchen', 'HRPQCT_UHR_NR', '071_F221272_HRPQCT', 'bone4_ROI_circle_5mm', roi_file)
maskPath = os.path.join('D:', 'd_users', 'Yuchen', 'HRPQCT_UHR_NR', '071_F221272_HRPQCT', 'bone4_ROI_circle_5mm', f'Single_Circle_thresholdnew1_{threshold}.nii')
```

Change these if your dataset is stored in a different location or folder.

---

### Output Directory

Set where to store feature results:

```python
base_save_dir = 'bone4_text_5mm'
```

Each threshold will create a subfolder under this path.

---

## Output

For each threshold combination:

- `features_matrix.npy`: All ROI features in a single array
- `feature_names.npy`: Feature name list
- `features_UHR_ROI_{i}_...npy`: Feature vector per ROI

---

## Notes

- Skips any ROI where image or mask is missing
- Reuses saved `.npy` files if already computed
- Frees memory with `gc.collect()` to reduce memory usage

---

## Example Output

```bash
Processing ROI_7 for threshold -600_800
Saved features: features_UHR_ROI_7_threshold_-600_800.npy
...
Processing complete.
```

# Evaluation of Extracted Features

This Jupyter notebook (`Evaluation.ipynb`) is designed to evaluate the texture features extracted from bone ROI data using PyRadiomics. It compares feature matrices against morphometric ground truth, performs correlation analysis, dimensionality reduction, and generates visualizations.

---

## Requirements

Ensure you have the following Python packages installed:

```bash
pip install numpy pandas matplotlib seaborn scikit-learn
```

---

## What the Notebook Does

The notebook includes the following steps:

1. **Load Feature Data**
   - Loads `.npy` files containing `features_matrix` and `feature_names` from each threshold folder.
   - Loads morphometric metrics (e.g., BV/TV, Tb.Th) from a CSV or text file.

2. **Data Preprocessing**
   - Concatenates feature matrices across thresholds or ROIs.
   - Optionally removes outliers or normalizes features.

3. **Correlation Analysis**
   - Computes Pearson correlation between features and target metrics.
   - Plots correlation heatmaps and scatter plots.

4. **Dimensionality Reduction**
   - Applies Lasso or PCA to reduce feature space.
   - Identifies important features per target metric.

5. **Model Evaluation**
   - Trains regression models (e.g., linear regression or SVR) to predict morphometric metrics from texture features.
   - Reports evaluation metrics like MAE, MSE, R², and CCC.

6. **Visualization**
   - Generates scatter plots of predicted vs. actual values.
   - Visualizes feature importance and residuals.

---

## How to Use

1. Launch Jupyter Notebook:
   ```bash
   jupyter notebook
   ```

2. Open `Evaluation.ipynb`.

3. Update the following:
   - Paths to your `features_matrix.npy`, `feature_names.npy`, and metric CSV file.
   - ROI ranges or filtering criteria.
   - Metric column names if different from default (e.g., `['BvTv', 'Tb.Th', 'Tb.Sp']`).

4. Run the cells sequentially.

---

## Input Files Required

- `features_matrix.npy`: Extracted features (N_ROIs × N_features)
- `feature_names.npy`: List of feature names
- `metrics.csv`: Morphometric ground truth (N_ROIs × N_metrics)

Example folder structure:

```
project/
│
├── threshold_folder/
│   ├── features_matrix.npy
│   ├── feature_names.npy
│
├── Evaluation.ipynb
├── metrics.csv
```

---

## Output

- Correlation matrices and heatmaps
- Plots showing best-correlated features
- Model performance scores
- Feature importance rankings

---

## Notes

- Ensure the order of ROIs in `features_matrix` and `metrics.csv` matches.
- You can modify the notebook to loop across multiple thresholds or combine them.

---

