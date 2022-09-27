%% CalculateConvectionCoeff: Calculates the convection coefficient and returns it and dimensionless numbers
function [Re,Pr,Nu,h] = CalculateConvectionCoeff(inDia,tubeLen,flowVel,kinVis,thermDiff,thermCond)
    % Reference: "Heat transfer in Flow Through Conduits", R. S. Subramanian,
    % Clarskson University
    
    Re = inDia*flowVel/kinVis;
    Pr = kinVis/thermDiff;
    
    if Re<2000
        %Use Sieder-Tate Correlation per Reference
        Nu = 3.66 + (0.065*Re*Pr*inDia/tubeLen)/(1+0.04*(Re*Pr*inDia/tubeLen)^(2/3));
    else
        % Assume transitional flow is described by turbulent flow. Use
        % Gnielinski Correlation per Reference
        f = 0.046*Re^(-0.2);
        Nu = ((f/2)*(Re-1000)*Pr)/(1 + 12.7*(Pr^(2/3)-1)*sqrt(f/2));
    end
    
    h = Nu*thermCond/inDia;
    
end