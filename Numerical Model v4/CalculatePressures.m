function [StressModel,StrainModel] = CalculatePressures(ModelParams,MatParams,RadiusList,StressModel,StrainModel,nodeLength)
    % Assign Params to Variables
    % --- Design Parameters
    
    %t_out = ModelParams(1);
    %t_in = ModelParams(2);
    r_out = ModelParams(3);
    r_in = ModelParams(4);
    %pipeLen = ModelParams(5);
    flowPres = ModelParams(6);
    %flowRate = ModelParams(7);
    
    % --- Material Paramters
    %tDiff = MatParams(1);
    %tCond = MatParams(2);
    %tExpa = MatParams(3);
    %kinVis = MatParams(4);
    elasticMod = MatParams(5);
    %poisson = MatParams(6);
    
    % Calculate constants
    d_out = 2 * r_out;
    d_in = 2 * r_in;
    
    % Calculate Pressure Stresses and radial strain
    for i = 1:length(RadiusList)
        r = RadiusList(i);
        
        StressModel(i,3) = (flowPres*(d_in/2)^2)/((d_out/2)^2-(d_in/2)^2) + ((d_in/2)^2*(d_out/2)^2*(-flowPres))/(r^2*((d_out/2)^2-(d_in/2)^2)); % Radial
        StressModel(i,4) = (flowPres*(d_in/2)^2)/((d_out/2)^2-(d_in/2)^2) - ((d_in/2)^2*(d_out/2)^2*(-flowPres))/(r^2*((d_out/2)^2-(d_in/2)^2)); % Hoop

        StrainModel(i,2) = StressModel(i,3)/elasticMod * nodeLength;
    end
    
end