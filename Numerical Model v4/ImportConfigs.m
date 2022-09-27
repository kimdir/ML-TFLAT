function [ToutList,TinList,RoutList,RinList,PipeLenList,FlowPresList,FlowRateList] = ImportConfigs(configFile)
    
    % Read data from spreadsheet into arrays, ignoring the first header row
    ConfigMatrix = readmatrix(configFile,"Range",[2,1]);
    
    ToutList = rmmissing(ConfigMatrix(:,1));
    TinList = rmmissing(ConfigMatrix(:,2));
    RoutList = rmmissing(ConfigMatrix(:,3));
    RinList = rmmissing(ConfigMatrix(:,4));
    PipeLenList = rmmissing(ConfigMatrix(:,5));
    FlowPresList = rmmissing(ConfigMatrix(:,6));
    FlowRateList = rmmissing(ConfigMatrix(:,7));
end