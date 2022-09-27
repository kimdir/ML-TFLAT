function totalCycles = CalculateCyclesWithTemp(stress,temp)
    % Equation viable for 6061 AL
    % Reference: "Effect of temperature on fatigue life behaviour of aluminium alloy AA6061 using analytical
    % approach" F. Hussain, S. Abdullah, M. Z. Nuwai. December 2016
    
    absTemp = temp + 274.15;
    sensCoeff = -0.0003*absTemp + 0.0805;    
    totalCycles = (stress/(651.8*absTemp^sensCoeff))^(-1/0.092);
    
end