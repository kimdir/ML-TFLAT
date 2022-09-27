function [TempModel,StressModel,StrainModel] = ThermalEquations(RadiusList,TempModel,StressModel,StrainModel,ModelParams,MatParams,b,h)
        %% Assign Params to Variables
    
    % --- Design Parameters
    t_out = ModelParams(1);
    t_in = ModelParams(2);
    %b = ModelParams(3)/2;
    a = ModelParams(4)/2;
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
    
    %% Thermal Equation
    % Calculate Thermal Equation Constants
    insideArea = 2*a*pi*pipeLen;
    heatFlux = h*insideArea*(t_out-t_in);
    stressCoeff = tExpa*elasticMod/(1-poisson);
    
    % Define Thermal Equation and Integrals
    thermGrad = @(r) heatFlux.*log(r.^2-a.^2)./(2.*pi.*tCond.*pipeLen) + t_in;
    thermGradIntegral = @(r) heatFlux.*log(r.^2-a.^2).*r./(2.*pi.*tCond.*pipeLen) + t_in;
    fullThermIntegral = integral(thermGradIntegral,b,a);
    
    % Loop through all radius points and calculate the temperature and thermal stresses and radial strain at each radius
    
    for i = 2:length(RadiusList)
        r = RadiusList(i);
        radiusThermIntegral = integral(thermGradIntegral,r,a);
        radiusThermGrad = thermGrad(r);
        
        TempModel(i) = thermGrad(r);
        
        % disp(size(StressModel))
        StressModel(i,1) = stressCoeff/r^2*(-1*radiusThermIntegral + (r^2-a^2)/(b^2-a^2)*fullThermIntegral); % Radial
        StressModel(i,2) = stressCoeff/r^2*(-1*radiusThermGrad*r^2 + radiusThermIntegral +(r^2+a^2)/(b^2-a^2)*fullThermIntegral); % Hoop
        StressModel(i,3) = stressCoeff*(-1*radiusThermGrad + (2*poisson)/(b^2-a^2)*fullThermIntegral); % Axial
        
        StrainModel(i,1) = tExpa/r * (1+poisson)/(1-poisson)*(radiusThermIntegral + ((1-2*poisson)*r^2+a)/(b^2-a^2)*fullThermIntegral);
    end
end
