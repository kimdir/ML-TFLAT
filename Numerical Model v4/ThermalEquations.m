function [TempModel,StressModel,StrainModel,isComplete] = ThermalEquations(RadiusList,TempModel,StressModel,StrainModel,ModelParams,MatParams,a,b,h)
        %% Assign Params to Variables
        % UPDATE v4: Importing a and b values instead of just a
    
    % --- Design Parameters
    t_out = ModelParams(1);
    t_in = ModelParams(2);
    %b = ModelParams(3)/2;
    %a = ModelParams(4)/2;
    pipeLen = ModelParams(5);
    % flowPres = ModelParams(6);
    % flowRate = ModelParams(7);
    
    % --- Material Paramters
    % tDiff = MatParams(1);
    tCond = MatParams(2);
    tExpa = MatParams(3);
    % kinVis = MatParams(4);
    elasticMod = MatParams(5);
    poisson = MatParams(6);
    
    % Initialize completion flag
    isComplete = 0;
    
    %% Thermal Equation
    % Calculate Thermal Equation Constants
    insideArea = 2*a*pi*pipeLen;
    heatFlux = h*insideArea*(t_out-t_in);
    stressCoeff = tExpa*elasticMod/(1-poisson);
    alpha = heatFlux/(2*pi*tCond*pipeLen);
    
    % Define Thermal Equation and Integrals
    thermGrad = @(r) t_in + alpha.*log(b/a).*(1-(log(r./b)./(log(a./b))));
    thermGradIntegral = @(r) (t_in + alpha.*log(b./a).*(1-(log(r./b)/(log(a./b))))).*r;
    fullThermIntegral = integral(thermGradIntegral,b,a);
    
    % Loop through all radius points and calculate the temperature and thermal stresses and radial strain at each radius
    % UPDATE v4: Added modification to update surface temperature and set
    % broken nodes to zero
    
    % Find surface node, assign it the inlet temperature and set broken
    % nodes to zero
    surfaceNode = find(RadiusList==a);
    
    if surfaceNode ~= 1
        for i = 1:surfaceNode
            TempModel(i) = 0;
        end
    end
    
    if surfaceNode  == length(RadiusList)
        isComplete = 1;
        return
    end
    TempModel(surfaceNode) = t_in;
    
    % Update temperatures for all viable nodes
    for i = surfaceNode+1:length(RadiusList)
        r = RadiusList(i);
        radiusThermIntegral = integral(thermGradIntegral,r,a);
        radiusThermGrad = thermGrad(r);
        
        TempModel(i) = thermGrad(r);
    end
    
    % Reference: "Thermal Stresses - Advanced Theory and Applications:
    % Chapter 6", Hetnarski, Richard B., Eslami, M. Reza, 2009
    
    for i = surfaceNode:length(RadiusList)        
        StressModel(i,1) = stressCoeff/r^2*(-1*radiusThermIntegral + (r^2-a^2)/(b^2-a^2)*fullThermIntegral); % Radial
        StressModel(i,2) = stressCoeff/r^2*(-1*radiusThermGrad*r^2 + radiusThermIntegral +(r^2+a^2)/(b^2-a^2)*fullThermIntegral); % Hoop
        StressModel(i,3) = stressCoeff*(-1*radiusThermGrad + (2*poisson)/(b^2-a^2)*fullThermIntegral); % Axial
        
        StrainModel(i,1) = tExpa/r * (1+poisson)/(1-poisson)*(radiusThermIntegral + ((1-2*poisson)*r^2+a)/(b^2-a^2)*fullThermIntegral);
    end
end
