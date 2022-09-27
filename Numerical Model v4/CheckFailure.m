function [isComplete,DamageModel] = CheckFailure(RadiusList,StressModel,DamageModel,MatParams,nodeLength)
    % Assign Material Parameters to Variables
    fracTough = MatParams(7);
    
    % Determine crack size based on DamageModel
    % UPDATE v4: Changed to search from inside out
    brokenNodes = 0;
    surfaceNode = 0;
    for i = 1:length(RadiusList)
        if DamageModel(i,2) == 1
            brokenNodes = brokenNodes + 1;
        else
            surfaceNode = i;
            break
        end
    end
    crackLength = brokenNodes * nodeLength;
    
    % Calculate Stress Intensity Factor
    SIF = StressModel(surfaceNode,6) * (pi * crackLength)^(1/2);
    DamageModel(:,3) = SIF;
    % Check SIF against fracture toughness to determine failure
    if SIF >= fracTough || brokenNodes == length(RadiusList)
        isComplete = 1;
    else
        isComplete = 0;
    end
end