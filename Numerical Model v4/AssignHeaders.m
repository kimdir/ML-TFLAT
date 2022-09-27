function OutputData = AssignHeaders(OutputData,RadiusList,repeatCount)
    for i = 2:length(OutputData(1,:))
        j = floor((i-2)/repeatCount)+1;
        OutputData(1,i) = RadiusList(j);
    end
end