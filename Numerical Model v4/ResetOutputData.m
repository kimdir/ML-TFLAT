function [TempData,StressData,StrainData,DamageData] = ResetOutputData(RadiusList,TempModel,StressModel,StrainModel,DamageModel,modelSize,cyclesToOutput)
    % Reset arrays to zero
    TempData = zeros(cyclesToOutput+1,length(TempModel(1,:))*modelSize+1);
    StressData = zeros(cyclesToOutput+1,length(StressModel(1,:))*modelSize+1);
    StrainData = zeros(cyclesToOutput+1,length(StrainModel(1,:))*modelSize+1);
    DamageData = zeros(cyclesToOutput+1,length(DamageModel(1,:))*modelSize+1);
    
    % Reestablish Header Values
    TempData = AssignHeaders(TempData,RadiusList,length(TempModel(1,:)));
    StressData = AssignHeaders(StressData,RadiusList,length(StressModel(1,:)));
    StrainData = AssignHeaders(StrainData,RadiusList,length(StrainModel(1,:)));
    DamageData = AssignHeaders(DamageData,RadiusList,length(DamageModel(1,:)));
    
end