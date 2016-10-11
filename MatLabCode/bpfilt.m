function y = bpfilt(signal, f1, f2, fs, isplot)
%% Bandpass filtering
%
% Syntax:
%   y = bpfilt(signal, f1, f2, [options])
%
% Description:
%   This function performs bandpass filtering of a time series 
%   with rectangle window.
%
% Input Arguments:
%   signal 	- a column vector of time series.
%   f1 		- the lower bound of frequencies (in Hz).
%   f2 		- the upper bound of frequencies (in Hz).
%
% Options:
%   fs      - the sampling frequency in Hz. Default is 1 Hz.
%   isplot  - whether to produce plots.
%
% Output Arguments:
%   y 		- the filtered time series.
%
% Examples:
%   fs = 100;
%   t  = 1:1/fs:10;
%   x  = sin(t);
%   y  = bpfilt(x,20,30);
%
% See also 
%
% References:
%
% History:
%   10/10/2016 - Initial script.
%

order    = 20; % relate with the singal length.
fcutlow  = f1;
fcuthigh = f2;
[b,a]    = butter(order,[fcutlow,fcuthigh]/(fs/2), 'bandpass');
y        = filtfilt(b,a,signal);