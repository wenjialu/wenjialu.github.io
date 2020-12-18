function [ ] = cds_simulation(pdata, odata, cplGMM, masterGMM, slaveGMM, dynamics)
%CDS_SIMULATION - performs the simulation with the given CDS models and
%various types of couplings

dt = 0.01;

figure('Color',[1 1 1]); 
axis([-0.2000         0   -0.2000         0         0    0.1400]);
hold on; grid on; view(-62,22);
xlabel('X Position');
ylabel('Y Position');
zlabel('Z Position');
pause;

% Starting from one of the demonstrations
demo_num = 2;
pos = pdata{demo_num}(:,1);         % Starting position - these are already substracted i.e. relative
                                    % Pose is in attractor frame
or  = odata{demo_num}(:,1);         % Starting orientation - not relative (not substracted)
otarget = odata{demo_num}(:,end);   % Target - from initial data
                                    
h  = PlotAxis(pos(:,end), or, 'aa', 0.1);
sp = plot3(pos(1,:)',pos(2,:)',pos(3,:)','-','Erasemode','none');
t=0;

pvel = GMR(masterGMM.Priors, masterGMM.Mu, masterGMM.Sigma, pos, 1:3, 4:6); % Computing initial pos velocity based on model
cplfnc = cplGMM.cplfunc;

while(norm(pvel) > 1e-2)  

    pos = [pos, pos(:,end) + dt*pvel];                      % Compute the next desired position by integrating velocity - Simulate position
    dor = GMR(cplGMM.Priors, cplGMM.Mu, cplGMM.Sigma, ...   % Compute the desired orientation based on coupling
        cplfnc(pos(:,end)), 1:cplGMM.coupl_dim, ...
        cplGMM.coupl_dim+1:size(cplGMM.Mu,1)) + otarget;    % Add the target orientation

    switch dynamics % dynamics type for the slave system
        case 'model_dyn'
            eor = GMR(slaveGMM.Priors, slaveGMM.Mu, slaveGMM.Sigma, or(:,end) - dor, 1:4, 5:8); % Compute orientation error
            or=[or, or(:,end) + 1*eor*dt];                                                      % Compute next orientation by integrating
        case 'linear_dyn'
            eor = (dor-or(:,end))*50; or=[or, or(:,end) + eor*dt];
        case 'no_dyn'
            or = [or, dor];
        otherwise 
            break;
    end
            
    set(sp, 'XData',pos(1,:),'YData',pos(2,:),'ZData',pos(3,:));

    delete(h);
    h=PlotAxis(pos(:,end), or(:,end), 'aa', 0.05);
    t=t+1;
    
    pvel = GMR(masterGMM.Priors, masterGMM.Mu, masterGMM.Sigma, pos(:,end), 1:3, 4:6); % Compute next velocity
    pause(0.001);
    
end

end

