function [ErrorCode] = ThermalFatigueModel(ModelParams,MatParams,Settings,modelID,outputFolder)

% Initialize Settings to variables
modelSize = Settings(1);
cyclesToOutput = Settings(2);
ErrorCode = 0;

% Initialize the model and check for validity
[isValid, RadiusList, TempModel, StressModel, StrainModel, DamageModel,nodeLength] = InitializeModel(ModelParams,modelSize);

% Break execution if configuration is invalid
if not(isValid)
    ErrorCode = 1;
    return
end

% Initialize Loop Variables
cycleCount = 0;
isComplete = false;

% Initialize Model Output Location
folderName = strcat(outputFolder,"/",mat2str(modelID));
mkdir(folderName)

[TempData,StressData,StrainData,DamageData] = ResetOutputData(RadiusList,TempModel,StressModel,StrainModel,DamageModel,modelSize,cyclesToOutput);

% Iterate until material failure
while not(isComplete)
    % Update Cycle Count
    cycleCount = cycleCount + 1;
    if mod(cycleCount,cyclesToOutput/10) == 0
        clc,sprintf("Cycle Count: %d", cycleCount)
    end
    
    % Calculate Temperatures, Stresses, and Strains
    [TempModel,StressModel,StrainModel,isComplete] = CalculateTemperatures(ModelParams,MatParams,RadiusList,TempModel,StressModel,StrainModel,DamageModel);
    
    if ~isComplete
        [StressModel,StrainModel] = CalculatePressures(ModelParams,MatParams,RadiusList,StressModel,StrainModel,nodeLength);
        [StressModel,StrainModel] = ProcessModels(StressModel,StrainModel);
        
        % Calculate Fatigue Effects
        [DamageModel] = CalculateDamage(RadiusList,TempModel,StressModel,DamageModel);
        
        % Check for Material Failure
        [isComplete,DamageModel] = CheckFailure(RadiusList,StressModel,DamageModel,MatParams,nodeLength);
        
        % Save model data to Output variables
        [TempData,StressData,StrainData,DamageData] = CollectOutputData(TempModel,StressModel,StrainModel,DamageModel,cycleCount,cyclesToOutput,TempData,StressData,StrainData,DamageData);
    end
    
    % Output model data at milestones
    if mod(cycleCount,cyclesToOutput) == 0 || isComplete
        OutputModelData(TempData,StressData,StrainData,DamageData,cycleCount,cyclesToOutput,folderName)
        [TempData,StressData,StrainData,DamageData] = ResetOutputData(RadiusList,TempModel,StressModel,StrainModel,DamageModel,modelSize,cyclesToOutput);
    end
end

% Save inputs to output folder for reference
inputPath = strcat(pwd,'/Config');
copyfile(inputPath,folderName)
end