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
