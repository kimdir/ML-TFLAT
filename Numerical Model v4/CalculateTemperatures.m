function [TempModel,StressModel,StrainModel,isComplete] = CalculateTemperatures(ModelParams,MatParams,RadiusList,TempModel,StressModel,StrainModel,DamageModel)
    
    %% Assign Params to Variables
    
    % --- Design Parameters
    %t_out = ModelParams(1);
    %t_in = ModelParams(2);
    outDia = ModelParams(3);
    inDia = ModelParams(4);
    pipeLen = ModelParams(5);
    %flowPres = ModelParams(6);
    flowRate = ModelParams(7);
    
    % --- Material Paramters
    tDiff = MatParams(1);
    tCond = MatParams(2);
    %tExpa = MatParams(3);
    kinVis = MatParams(4);
    %elasticMod = MatParams(5);
    %poisson = MatParams(6);
    
    %% Dimensionless Numbers
    % Calculate Dimensionless Number Constants
    %inDia = r_in * 2;
    flowVel = flowRate/((inDia/2)^2*pi());
    
    % Calculate Dimensionless Numbers and Convection Coefficient
    [~,~,~,h] = CalculateConvectionCoeff(inDia,pipeLen,flowVel,kinVis,tDiff,tCond);
    
    %% Temperatures and Thermal Stresses
    % UPDATE v4: Changed to find minimum a instead of max b
    % Find min value for a (Changes as damage increases)
    for i = 1:length(RadiusList)
        if DamageModel(i,2) == 0
            a = RadiusList(i);
            break
        end
    end
    
    b = outDia/2;
    
    % Calculate Temperatures and Thermal Stresses
    [TempModel,StressModel,StrainModel,isComplete] = ThermalEquations(RadiusList,TempModel,StressModel,StrainModel,ModelParams,MatParams,a,b,h);
end