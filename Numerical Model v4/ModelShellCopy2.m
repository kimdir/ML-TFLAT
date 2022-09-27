clc;

% Define Inputs and Outputs
configFile = 'Config3/ModelConfigurations.xls';
matFile = 'Config3/MaterialParameters.xls';
settingsFile = 'Config3/Settings.xls';

currentTime = strrep(datestr(now),':','-');
outputFolder = strcat(pwd,"/Outputs/",currentTime);
mkdir(outputFolder)

% Import configuration values and parameters
updateOpt = input("Update inputs?");
if updateOpt
    configOpt = input("Update configurations?");
    matOpt = input("Update material properties?");
    setOpt = input("Update settings?");
    
    if configOpt || matOpt || setOpt
        WriteConfigs([configOpt,matOpt,setOpt],configFile,matFile,settingsFile)
    end
end


[ToutList,TinList,RoutList,RinList,PipeLenList,FlowPresList,FlowRateList] = ImportConfigs(configFile);
[MatParams,Settings] = ImportParams(matFile,settingsFile);

% Initialize error code tracking array
totalConfigs = length(TinList)*length(ToutList)*length(RinList)*length(RoutList)*length(PipeLenList)*length(FlowPresList)*length(FlowRateList);
errorLog = zeros(totalConfigs,2);
configCount = 0;

sprintf("Total Configs: %d",totalConfigs)

% Iterate through configurations
for xTout = 1:length(ToutList)
    for xTin = 1:length(TinList)
        for xRout = 1:length(RoutList)
            for xRin = 1:length(RinList)
                for xPipeLen = 1:length(PipeLenList)
                    for xFlowPres = 1:length(FlowPresList)
                        for xFlowRate = 1:length(FlowRateList)
                            
                            % Generate Model ID
                            modelID = [xTout,xTin,xRout,xRin,xPipeLen,xFlowPres,xFlowRate];
                            configCount = configCount + 1;
                            
                            % Assign model configuration to ModelParam array variables
                            Tin = TinList(xTin);
                            Tout = ToutList(xTout);
                            Rin = RinList(xRin);
                            Rout = RoutList(xRout);
                            PipeLen = PipeLenList(xPipeLen);
                            FlowPres = FlowPresList(xFlowPres);
                            FlowRate = FlowRateList(xFlowRate);
                            
                            ModelParams = [Tout,Tin,Rout,Rin,PipeLen,FlowPres,FlowRate];
                            
                            % Run the model and record error codes
                            [ErrorCode] = ThermalFatigueModel(ModelParams,MatParams,Settings,modelID,outputFolder);
                            errorLog(configCount,:) = [string(mat2str(modelID)),ErrorCode];
                            
                        end
                    end
                end
            end
        end
    end
end

% Check for number of completed model runs and print result statement
resultStatement = 'Successful Model Runs: %d / %d (%g%%)';
totalSuccessful = totalConfigs-nnz(ErrorLog(:,2));
pctComplete = (totalSuccessful)/totalConfigs;
sprintf(resultStatement,totalSuccessful,totalConfigs,pctComplete)
writematrix(ErrorLog,strcat(outputFolder,"/_Error Log.xls"))
