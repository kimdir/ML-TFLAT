function [MatParams,Settings] = ImportParams(matFile,settingsFile)
    
    % Import Material Parameters, ignoring first column labels and first
    % row header
    
    MatParams = readmatrix(matFile,"Range",[1,2]);
    
    % Import Settings, ignoring first column labels
    
    Settings = readmatrix(settingsFile,"Range",[1,2]);
end