function [StressModel,StrainModel] = ProcessModels(StressModel,StrainModel)
    
    % Calculate Von Mises Stresses
    StressModel = CalculateVonMises(StressModel);
    
    % Calculate total radial strain
    StrainModel(:,3) = StrainModel(:,1) + StrainModel(:,2);
    
end