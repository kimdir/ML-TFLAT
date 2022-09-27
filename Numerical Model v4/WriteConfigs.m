%%% WriteConfigs: Used to write data to .xls files through matlab
%%% (For use with Matlab Online, potential integration with main)

function WriteConfigs(options,configFile,matFile,settingsFile)
    % Define File Names and delete old config files
    
    if isfile(configFile), delete configFile, end
    if isfile(matFile), delete matFile, end
    if isfile(settingsFile), delete settingsFile, end
    
    %% Config File
    if options(1) ~= 0
        % Request configuration input
        ToMin = input('Minimum Outlet Temperature?');   clc;
        ToMax = input('Maximum Outlet Temperature?');   clc;
        ToCount = input('Count of Outlet Temperature?');clc;
        
        TiMin = input('Minimum Inlet Temperature?');    clc;
        TiMax = input('Maximum Inlet Temperature?');    clc;
        TiCount = input('Count of Inlet Temperature?'); clc;
        
        RoMin = input('Minimum Outer Radius?');         clc;
        RoMax = input('Maximum Outer Radius?');         clc;
        RoCount = input('Count of Outer Radius?');      clc;
        
        RiMin = input('Minimum Inner Radius?');         clc;
        RiMax = input('Maximum Inner Radius?');         clc;
        RiCount = input('Count of Inner Radius?');      clc;
        
        PLMin = input('Minimum Pipe Length?');          clc;
        PLMax = input('Maximum Pipe Length?');          clc;
        PLCount = input('Count of Pipe Length?');       clc;
        
        FPMin = input('Minimum Flow Pressure?');        clc;
        FPMax = input('Maximum Flow Pressure?');        clc;
        FPCount = input('Count of Flow Pressure?');     clc;
        
        FRMin = input('Minimum Flow Rate?');            clc;
        FRMax = input('Maximum Flow Rate?');            clc;
        FRCount = input('Count of Flow Rate?');         clc;
        
        % Assemble configuration lists
        configLabels = ['Temp Out','Temp In','Outer Radius','Inner Radius','Pipe Length','Flow Pressure','Flow Rate'];
        ToutList = linspace(ToMin,ToMax,ToCount)';
        TinList = linspace(TiMin,TiMax,TiCount)';
        RoutList = linspace(RoMin,RoMax,RoCount)';
        RinList = linspace(RiMin,RiMax,RiCount)';
        PipeLenList = linspace(PLMin,PLMax,PLCount)';
        FlowPresList = linspace(FPMin,FPMax,FPCount)';
        FlowRateList = linspace(FRMin,FRMax,FRCount)';
        
        % Write configurations to .xls file
        writematrix(configLabels,configFile,"Range",'A1:G1')
        writematrix(ToutList,configFile,"Range",'A2')
        writematrix(TinList,configFile,"Range",'B2')
        writematrix(RoutList,configFile,"Range",'C2')
        writematrix(RinList,configFile,"Range",'D2')
        writematrix(PipeLenList,configFile,"Range",'E2')
        writematrix(FlowPresList,configFile,"Range",'F2')
        writematrix(FlowRateList,configFile,"Range",'G2')
        
        % Summary
        sprintf("Total Configurations: %d",(ToCount*TiCount*RoCount*RiCount*PLCount*FPCount*FRCount))
    end
    
    
    %% Material Parameters
    if options(2) ~= 0
        
        % Input values to variables
        tDiff = input("Thermal Diffusivity? (m^2/s) "); clc;
        tCond = input("Thermal Conductivity? (W/mK) "); clc;
        tExpa = input("Thermal Expansion Coefficient? (m/mK) "); clc;
        kinVis = input("Fluid Kinematic Viscosity? (m^2/s) "); clc;
        eMod = input("Elastic Modulus? (MPa) "); clc;
        pRatio = input("Poisson's Ratio? "); clc;
        frTough = input("Fracture toughness? (MPA*m^(1/2) "); clc;
        
        % Write variables to .xls file
        matLabels = ['Thermal Diffusivity [Al] (m^2/s)','Thermal Conductivity [Al] (W/(mK))','Thermal Expansion [Al] (m/(m*K))','Kinetic Viscosity [Water] (m^2/s)','Elastic Modulus [Al] (MPa)',"Poisson's Ratio [Al] (---)",'Fracture Toughness [Al] (MPa*m^(1/2))']';
        matParams = [tDiff,tCond,tExpa,kinVis,eMod,pRatio,frTough]';
        writematrix(matLabels,matFile,"Range",'A1')
        writematrix(matParams,matFile,"Range",'B1')
    end
    %% Settings
    if options(3) ~= 0
        
        % Input data to variables
        
        modelSize = input("Number of Nodes? "); clc;
        cyclesToOutput = input("Number of cycles to output per data load? "); clc;
        
        % Write variables to .xls
        SettingsLabels = ['Number of nodes','Number of cycles per data output']';
        Settings = [modelSize,cyclesToOutput]';
        
        writematrix(SettingsLabels,settingsFile,"Range",'A1')
        writematrix(Settings,settingsFile,"Range",'B1')
    end
    
end