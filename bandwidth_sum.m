format long;

% 
% ftime_50 = 432.592218;
% sfog_50len = [46,60,61];
% sfog_50count = [2931,580,2352];
% cfog_50len = [54,60,461];
% cfog_50count = [1,45,43];
% 
% ftime_100 = 433.598505;
% sfog_100len = [46,60,61];
% sfog_100count = [3012,300,2713];
% cfog_100len = [54,60,861];
% cfog_100count = [1,45,43];
% 
% ftime_150 = 431.523911;
% sfog_150len = [46,60,61,62];
% sfog_150count = [2956,198,1760,999];
% cfog_150len = [60,1261];
% cfog_150count = [43,43];
% 
% ftime_200 = 431.503602;
% sfog_200len = [46,60,61,62];
% sfog_200count = [3019,150,1369,1500];
% cfog_200len = [54,60,201,1514];
% cfog_200count = [1,45,43,43];
% 
% ftime_250 = 435.553589;
% sfog_250len = [46,60,61,62];
% sfog_250count = [3016,120,1080,1816];
% cfog_250len = [54,60,601,1514];
% cfog_250count = [1,45,43,43];
% 
% [bandwidth_50_s_f] = bandwidth_calc(sfog_50len,sfog_50count,ftime_50)
% [bandwidth_50_f_c] = bandwidth_calc(cfog_50len,cfog_50count,ftime_50)
% 
% [bandwidth_100_s_f] = bandwidth_calc(sfog_100len,sfog_100count,ftime_100)
% [bandwidth_100_f_c] = bandwidth_calc(cfog_100len,cfog_100count,ftime_100)
% 
% [bandwidth_150_s_f] = bandwidth_calc(sfog_150len,sfog_150count,ftime_150)
% [bandwidth_150_f_c] = bandwidth_calc(cfog_150len,cfog_150count,ftime_150)
% 
% [bandwidth_200_s_f] = bandwidth_calc(sfog_200len,sfog_200count,ftime_200)
% [bandwidth_200_f_c] = bandwidth_calc(cfog_200len,cfog_200count,ftime_200)
% 
% [bandwidth_250_s_f] = bandwidth_calc(sfog_250len,sfog_250count,ftime_250)
% [bandwidth_250_f_c] = bandwidth_calc(cfog_250len,cfog_250count,ftime_250)

 mqtttime_50 = 446.814874;
 mqtt_50len = [54,56,60,68];
 mqtt_50count = [33853,2,4,33853];
 
 mqtttime_100 = 437.966934;
 mqtt_100len = [54,56,60,68];
 mqtt_100count = [32979,1,52,32876];
 
 mqtttime_150 = 436.788019;
 mqtt_150len = [54,56,60,68];
 mqtt_150count = [32662,1,103,32561];
 
 mqtttime_200 = 434.425779;
 mqtt_200len = [54,56,60,68];
 mqtt_200count = [32961,1,153,32810];
 
 mqtttime_250 = 434.679767;
 mqtt_250len = [54,56,60,68];
 mqtt_250count = [32494,1,203,32291];
 
 mqtttime_300 = 434.780475;
 mqtt_300len = [54,56,60,68];
 mqtt_300count = [32813,1,2,32812];;

 [bandwidth_50_s_c] = bandwidth_calc(mqtt_50len,mqtt_50count,mqtttime_50)
 [bandwidth_100_s_c] = bandwidth_calc(mqtt_100len,mqtt_100count,mqtttime_100)
 [bandwidth_150_s_c] = bandwidth_calc(mqtt_150len,mqtt_150count,mqtttime_150)
 [bandwidth_200_s_c] = bandwidth_calc(mqtt_200len,mqtt_200count,mqtttime_200)
 [bandwidth_250_s_c] = bandwidth_calc(mqtt_250len,mqtt_250count,mqtttime_250)
 [bandwidth_300_s_c] = bandwidth_calc(mqtt_300len,mqtt_300count,mqtttime_300)


function [band] = bandwidth_calc(c_arr, s_arr, time)
len = length(c_arr);
tot_sum = 0;
for i = 1:len
    tot_sum = tot_sum + (c_arr(i) * s_arr(i));
end
band = tot_sum / time;
end
