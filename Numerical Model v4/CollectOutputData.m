function [TempData,StressData,StrainData,DamageData] = CollectOutputData(TempModel,StressModel,StrainModel,DamageModel,cycleCount,cyclesToOutput,TempData,StressData,StrainData,DamageData)
    % Calculate Index for data
    cycleIndex = mod(cycleCount,cyclesToOutput)+1;
    
    % Adjust so that header row is not overwritten
    if cycleIndex == 1
        cycleIndex = cyclesToOutput+1;
    end
    
    % Assign cycle number to all data sets
    TempData(cycleIndex,1) = cycleCount;
    StressData(cycleIndex,1) = cycleCount;
    StrainData(cycleIndex,1) = cycleCount;
    DamageData(cycleIndex,1) = cycleCount;
    
    % Assign Temperature Data
    TempData(cycleIndex,2:length(TempData(1,:))) = TempModel(:)';
    
    % Assign Stress Data
    StressData(cycleIndex,2:length(StressData(1,:))) = reshape(StressModel',1,[]);
    
    % Assign Strain Data
    StrainData(cycleIndex,2:length(StrainData(1,:))) = reshape(StrainModel',1,[]);
    
    % Assign Damage Data
    DamageData(cycleIndex,2:length(DamageData(1,:))) = reshape(DamageModel',1,[]);
end