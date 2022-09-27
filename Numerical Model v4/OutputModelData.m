function OutputModelData(TempData,StressData,StrainData,DamageData,cycleCount,cyclesToOutput,folderName)
% Create output folders if nonexistant
tempDir = strcat(folderName,'/Temperature');
stressDir = strcat(folderName,'/Stress');
strainDir = strcat(folderName,'/Strain');
damageDir = strcat(folderName,'/Damage');

if ~exist(tempDir,'dir')
    mkdir(tempDir)
end

if ~exist(stressDir,'dir')
    mkdir(stressDir)
end

if ~exist(strainDir,'dir')
    mkdir(strainDir)
end

if ~exist(damageDir,'dir')
    mkdir(damageDir)
end
    
% Output indicator to command window
    sprintf("Data output @ %d cycles",cycleCount)
    
    % Determine the Data Part #
    partNum = ceil(floor(cycleCount)/cyclesToOutput);
    
    % Assign file paths for outputs
    tempPath = strcat(tempDir,'/Temperature - Part ',num2str(partNum),'.csv');
    stressPath = strcat(stressDir,'/Stress - Part ',num2str(partNum),'.csv');
    strainPath = strcat(strainDir,'/Strain - Part ',num2str(partNum),'.csv');
    damagePath = strcat(damageDir,'/Damage - Part ',num2str(partNum),'.csv');
    
    % Write matrices to .csv files
    writematrix(TempData,tempPath);
    writematrix(StressData,stressPath);
    writematrix(StrainData,strainPath);
    writematrix(DamageData,damagePath);
end