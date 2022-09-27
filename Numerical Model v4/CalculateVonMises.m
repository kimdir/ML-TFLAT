function [StressModel] = CalculateVonMises(StressModel)
    
    % Loop through all nodes in the model
    for i = 1:length(StressModel(:,1))
      
        % Sum radial and tangential stresses, and assign all to holder variables
        radS = StressModel(i,1) + StressModel(i,4);
        tanS = StressModel(i,2) + StressModel(i,5);
        axiS = StressModel(i,3);
        
        % Calculate von Mises stress
        StressModel(i,6) = sqrt(((radS+tanS)^2 + (tanS+axiS)^2 + (axiS + radS)^2)/2);
    end
end