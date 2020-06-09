function [cds_learning_parameters] = cds_set_learning_parameters( )
%CDS_SET_LEARNING_PARAMETERS Sets the parameters for learning the amster
%and slave dynamics. 

%% Master Parameters 

% === General parameters ===
cds_learning_parameters.master.K    = 1;           % Number of Gaussian functions
cds_learning_parameters.master.dt   = 0.001*10;   % sampling frequency of the data x the decimation factor used when loading
cds_learning_parameters.master.tol  = 0.2;       % Tolerance factor for cutting the demos

% === Solver parameters ===

% A set of options that will be passed to the solver. Please type 'doc
% preprocess_demos' in the MATLAB command window to get detailed
% information about each option.

options=[];
options.tol_mat_bias    = 10^-6;   % to avoid instabilities in the gaussian kernel
options.perior_opt      = 0;
options.mu_opt          = 1;       % optimize centers
options.sigma_x_opt     = 1;
options.display         = 1;
options.tol_stopping    = 10^-10;
options.max_iter        = 5000;
options.normalization   = 1;
options.objective       = 'likelihood';
options.cons_penalty    = 1e10; % penalty for not going straight to the attractor. 
                                % Increase to obtain a more straight line

cds_learning_parameters.master.solver_options = options;
clear options; 

% === Simulator parameters === 

opt_sim.dt      = 0.01;
opt_sim.i_max   = 3000;
opt_sim.tol     = 0.001;

cds_learning_parameters.master.sim_options = opt_sim;
clear opt_sim;

%% Slave Parameters 

% === General parameters ===
cds_learning_parameters.slave.K     = 1;           % Number of Gaussian functions
cds_learning_parameters.slave.dt    = 0.001*10;   % sampling frequency of the data x the decimation factor used when loading
cds_learning_parameters.slave.tol   = 0.0;       % Tolerance factor for cutting the demos

% === Solver parameters ===

% A set of options that will be passed to the solver. Please type 'doc
% preprocess_demos' in the MATLAB command window to get detailed
% information about each option.
options.tol_mat_bias    = 10^-6;
options.perior_opt      = 1;
options.mu_opt          = 1;
options.sigma_x_endopt  = 1;
options.display         = 1;
options.tol_stopping    = 10^-10;
options.max_iter        = 5000;
options.normalization   = 1;
options.objective       = 'likelihood';
options.cons_penalty    = 1e10;

cds_learning_parameters.slave.solver_options = options;
clear options; 

% === Simulator parameters === 
opt_sim.dt              = 0.02;
opt_sim.i_max           = 3000;
opt_sim.tol             = 0.001;

cds_learning_parameters.slave.sim_options = opt_sim;
clear opt_sim;

%% Save params
save('cds_learning_parameters.mat','cds_learning_parameters','-mat');

end

