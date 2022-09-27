function [DamageModel] = CalculateDamage(RadiusList,TempModel,StressModel,DamageModel)
    % Cycle through nodes to calculate damage
    for i = 1:length(RadiusList)
        
        % Skip node if failed
        if DamageModel(i,2) == 1
            continue;
        end
        
        % Calculate max cycles at temp and add 1 cycle of percent damage to DamageModel
        nodeCycles = CalculateCyclesWithTemp(TempModel(i),StressModel(i,6));
        DamageModel(i,1) = DamageModel(i,1) + 1/nodeCycles;
        
        % Check if node has failed
        if DamageModel(i,1) >= 1
            DamageModel(i,2) = 1;
        end
    end
end