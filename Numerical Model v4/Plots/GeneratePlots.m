% Generate Plots

% Varied Inlet Temp External Node Damage Graph
%GetInTempDamage

classNames = ['InTemp','OutTemp','WallThick','Length','Pressure','FlowRate'];
classTitles = ['Varying Inlet Temperature', 'Varying Outlet Temperature', 'Varying Wall Thickness', 'Varying Pipe Length', 'Varying Pressure', 'Varying Flow Rate'];

%% Convergence Plot
GetConvergence;
ConvergeArray = table2array(ConvergeData);
figure
hold on
title("Model Convergence Analysis")
subplot(1,2,1)
plot(ConvergeArray(:,1),ConvergeArray(:,2),'-x')
xlabel('Nodes'), ylabel('Cycles To Failure')
grid ON
% subplot(1,3,2)
% plot(ConvergeArray(:,1),ConvergeArray(:,3),'-x')
% xlabel('Nodes'), ylabel('Change in Cycles To Failure')
% grid ON
subplot(1,2,2)
plot(ConvergeArray(:,1),ConvergeArray(:,4).*100,'-x')
xlabel('Nodes'), ylabel('Percent Change in Cycles To Failure')
grid ON
hold off



%% Function Definitions
function GetData(className,classTitle)
dataTypes = ['Damage','Stress','Strain','Temp'];
dataUnits = ['% Total Life', 'MPa', '°C'];
plotTypes = ['linear','logx','logy','loglog'];

for j = 1:length(dataTypes)
    data = table2array(run(concat('Get',className,dataTypes(j))));
    variableNames = data.Properties.VariableNames();
    axisLabels = ['Cycles',concat(dataTypes(j),' - ',dataUnits(j))];
    
    plotType = plotTypes(1); % Change if not linear
    
    plotTitle = concat(classTitle,' - ',dataTypes(j));
    lineOpts = ['','','--',':'];
    
    if strcmp(plotType, 'linear')
        LinearPlot(data,plotTitle,lineOpts,variableNames,axisLabels)
    elseif strcmp(plotType,'logx')
        LogXPlot(data, plotTitle, lineOpts, variableNames,axisLabels)
    elseif strcmp(plotType,'logy')
        LogYPlot(data, plotTitle, lineOpts, variableNames,axisLabels)
    elseif strcmp(plotType,'loglog')
        LogLogPlot(data, plotTitle, lineOpts, variableNames,axisLabels)
    end
end
end

function LinearPlot(data, plotTitle, lineOpts, variableNames,axisLabels)
figure
hold on
for i = 2:length(data(1,:))
    plot(data(:,1),data(:,i),lineOpts(i))
end

title(plotTitle);
legend(variableNames);
xlabel(axisLabels(1));
ylabel(axisLabels(2));

hold off
end

function LogXPlot(data, plotTitle, lineOpts, variableNames,axisLabels)
figure
hold on
for i = 2:length(data(1,:))
    semilogx(data(:,1),data(:,i),lineOpts(i))
end

title(plotTitle);
legend(variableNames);
xlabel(axisLabels(1));
ylabel(axisLabels(2));

hold off
end

function LogYPlot(data, plotTitle, lineOpts, variableNames,axisLabels)
figure
hold on
for i = 2:length(data(1,:))
    semilogy(data(:,1),data(:,i),lineOpts(i))
end

title(plotTitle);
legend(variableNames);
xlabel(axisLabels(1));
ylabel(axisLabels(2));

hold off
end

function LogLogPlot(data, plotTitle, lineOpts, variableNames,axisLabels)
figure
hold on
for i = 2:length(data(1,:))
    loglog(data(:,1),data(:,i),lineOpts(i))
end

title(plotTitle);
legend(variableNames);
xlabel(axisLabels(1));
ylabel(axisLabels(2));

hold off
end