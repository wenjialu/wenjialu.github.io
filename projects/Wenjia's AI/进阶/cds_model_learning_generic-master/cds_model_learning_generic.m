% Create CDS Models of position and orientation

% !!! update your learning parameters in cds_learning_parameters

[pdata, odata, odata_dyn, otarget] = cds_load_data(); % Load raw data
load('cds_learning_parameters.mat');                  % Load learning parameters

cplGMM      = cds_learn_coupling(pdata, odata, odata_dyn);
masterGMM   = cds_learn_master(pdata, cds_learning_parameters);
slaveGMM    = cds_learn_slave(odata_dyn, otarget, cds_learning_parameters);

cds_save_models;

cds_simulation(pdata, odata, cplGMM, masterGMM, slaveGMM, 'model_dyn');



