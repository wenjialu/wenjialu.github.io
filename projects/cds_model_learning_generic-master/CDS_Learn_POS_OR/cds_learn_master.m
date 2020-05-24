function [masterGMM] = cds_learn_master(pdata, params)
%CDS_LEARN_MASTER learns the master dynamics (3D position, 3D velocity)

%% Model learning
% Preprocess substracted position data.
[x0 , xT, Data, index] = preprocess_demos(pdata, params.master.dt, params.master.tol);         

% Find an initial guess for GMM's parameter                                          
[Priors, Mu, Sigma] = initialize_SEDS(Data, params.master.K);                    

% Run the SEDS optimization solver
[Priors Mu Sigma]=SEDS_Solver(Priors,Mu,Sigma,Data,params.master.solver_options); 

masterGMM           = [];
masterGMM.Priors    = Priors;
masterGMM.Mu        = Mu;
masterGMM.Sigma     = Sigma;
masterGMM.States    = params.master.K;


%% Run the simulation

% Start from a given demonstration and/or add a little offset
x0_all = Data(1:3,index(1:end-1)) + 0.01 * randn(3,length(index)-1); 

fn_handle = @(y) GMR(Priors,Mu,Sigma,y,1:3,4:6);
[x, xd, tmp, xT] = Simulation(x0_all,[], fn_handle, params.master.sim_options); 
 
end

