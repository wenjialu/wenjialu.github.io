function [ slaveGMM ] = cds_learn_slave(odata_dyn, otarget, params)
%CDS_LEARN_SLAVE Learns the slave dynamics from a given 

%% Model learning

%Preprocessing
[x0 , xT, Data, index] = preprocess_demos(odata_dyn, params.slave.dt, params.slave.tol);
% Find an initial guess for GMM's parameter
[Priors, Mu, Sigma] = initialize_SEDS(Data, params.slave.K); 
% Run the SEDS optimization solver
[Priors Mu Sigma] = SEDS_Solver(Priors, Mu, Sigma, Data, params.slave.solver_options); 

slaveGMM        = [];
slaveGMM.Priors = Priors;
slaveGMM.Mu     = Mu;
slaveGMM.Sigma  = Sigma;
slaveGMM.States =  params.slave.K;

%% Run the simulator
x0_all = Data(1:4,index(1:end-1)); % Start from a given demo

fn_handle = @(y) GMR(Priors, Mu, Sigma, y, 1:4, 5:8); % Initialize GMR 
[x, xd, tmp, xT]= Simulation(x0_all,[], fn_handle, params.slave.sim_options); 

%% Plotting
figure(3); subplot(1,2,1); cla; hold on
plot(x(:,:,2)');
subplot(1,2,2); cla; hold on;
plot(odata_dyn{1}'); plot(odata_dyn{2}'); plot(odata_dyn{3}');

% Check how much the orientation changed
figure(4); cla; hold on;
axis([-1 1 -1 1 -1 1]);
for i=1:10:size(x,2)
   disp(i);
   PlotAxis([0;0;0], x(:,i,1) + otarget, 'aa',0.5);
   pause(0.01);
end

end

