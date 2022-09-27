function [isValid, RadiusList, TempModel, StressModel, StrainModel, DamageModel,nodeLength] = InitializeModel(ModelParams,ModelSize)
    % UPDATE v4: Added extra column to DamageModel to account for SIF
    % output
    
    % Assign Model Paramters --- >>> Update if Changed <<<
    t_out = ModelParams(1);
    t_in = ModelParams(2);
    d_out = ModelParams(3);
    d_in = ModelParams(4);
    pipeLen = ModelParams(5);
    flowPres = ModelParams(6);
    flowRate = ModelParams(7);
    
    % Check for valid configuration
    tCheck = t_out < t_in;
    rCheck = d_out > d_in;
    lenCheck = pipeLen > 0;
    presCheck = flowPres > 0;
    flowCheck = flowRate > 0;
    
    isValid = tCheck & rCheck & lenCheck & presCheck & flowCheck;
    
    % Build Model Arrays --- Array size zero for invalid configurations
    RadiusList = linspace(d_in/2,d_out/2,ModelSize*isValid);
    TempModel = zeros(isValid*ModelSize,1);
    StressModel = zeros(isValid*ModelSize,6);
    StrainModel = zeros(isValid*ModelSize,3);
    DamageModel = zeros(isValid*ModelSize,3);
    
    nodeLength = RadiusList(2)-RadiusList(1);
    
end