from readBHspc import readBHspc
import numpy as np
from fitPowerLaw import fitPowerLaw
from filterAP import filterAP


def removeAfterpulse(filename, tau, ks, b, nseg, dt, Lseg=200000):
    
    [data, info] = readBHspc(filename)
    
    # calculate absolute macrotimes
    time = data[:, 0]
    time = (time - np.min(time)) * info.macrotime
    totTime = np.max(time)
    
    # calculate absolute microtimes
    # microtime = 4096 - lags (4096 bins in total)
    # microTime = 4096 - data[:, 1]
    microTime = data[:, 1] * info.microtime
    
    # plot intensity trace
    maxseg = int(np.floor(totTime / info.macrotime / Lseg))
    [Itrace, timeBins] = np.histogram(time, maxseg)
    
    plt.figure()
    plt.plot(timeBins[0:-1], Itrace)
    plt.ylim([0, 600])
    plt.xlim([0, np.max(timeBins)])
    plt.xlabel("Time [s]")
    plt.ylabel("#photons per bin of " + '{:.1f}'.format(timeBins[1]*1000) + " ms")
    
    # plot histogram
    [Ihist, lifetimeBins] = np.histogram(microTime, info.microtime * np.linspace(0, 4096, int(4096/16+1)))
    
    plt.figure()
    plt.plot((lifetimeBins[0:-1]-lifetimeBins[0]) / lifetimeBins[1], Ihist)
    plt.xlabel("Time [s]")
    plt.ylabel("#photons per bin of " + '{:.1f}'.format(lifetimeBins[1]*1e12) + " ps")
    
    # find index peak and zoom
    idxStart = np.where(Ihist == np.max(Ihist))[0][0]
    idxStop = np.where(Ihist == np.min(Ihist[210:219]))[0][0] + 1
    T = 209 + idxStop - idxStart
    
    lifetimeBinsFit = 1e9 * (lifetimeBins[idxStart:idxStop]-lifetimeBins[idxStart]) # ns
    # normalize time?
    lifetimeBinsFit = lifetimeBinsFit / lifetimeBinsFit[1]
    IhistFit = Ihist[idxStart:idxStop]
    plt.figure()
    plt.scatter(lifetimeBinsFit, IhistFit)
    plt.xlabel("Time [a.u.]")
    plt.ylabel("#photons per bin of " + '{:.1f}'.format(lifetimeBins[1]*1e12) + " ps")
    plt.xlim([0, lifetimeBinsFit[-1]])
    plt.ylim([0, IhistFit[0]])
    
    fitresult = fitPowerLaw(IhistFit, lifetimeBinsFit, 'exp', [1, 1, 1], [60000, 4, 0], [0, 0, -1e4], [1e6, 20, 1e6])
    A = fitresult.x[0]
    alpha = fitresult.x[1]
    B = fitresult.x[2]
    plt.plot(lifetimeBinsFit, A * np.exp(-alpha * lifetimeBinsFit) + B, color='r')
    
    
    
    
    
    if ks==0:
        param=FitExp((1:1:T),Icut(1:T),1);
        tau=param(3);
        b=param(1);
    else:
        param=FitExpK_for_ap((1:1:T),Icut(1:T),ks,tau,1);
        ks=param(3);
        tau=param(4);
        b=param(1);
    end
        
    % [param, n]=FitExp((t0+1:t0+T),Icut,0);
    
    A=zeros(1,Lseg,256);
    Y=1;
    X=Lseg;
    
    nc=2;
    harm=1;
    
    [filter1]=filter_enderlein_ap(ks, tau, T, 1,1,b);
    
    filtshape=squeeze(filter1(1,1,:,:));
    filter=repmat(filter1, Y,X,1,1);    
    
    i=minseg;
    [count, ~, ~, ~] = histcn( F,dt.*(Lseg*(i-1):Lseg*(i)),0:16:4096 );
    A(1,:,:)=count(1:Lseg,1:256);
    clear count;
    A=double(A(:,:,t0+1:t0+T));
    % Ag=A(:,:,Tg:T);
    Ntot=sum(A,3);
    % Ng=sum(Ag,3);
    Nlog=256;
    [ACFlog, taulog, ~, ~]=FCS_imgdata(Ntot,dt,0,Nlog);
    % [ACFglog, taulog, ~, ~]=FCS_imgdata(Ng,dt,0,Nlog);
    Ns=zeros(size(A,1),size(A,2),nc);
    ACF1log=zeros(1);
    for k=1:nc    
    
    Ns(:,:,k)=sum(filter(:,:,:,k).*A,3);
    [temp, taulog, ~, ~]=FCS_imgdata(Ns(:,:,k),dt,0,Nlog);
    ACF1log(k,1:length(temp))=temp;
    end
    clear A;    
    % Ntotap=sum(Ns(:,:,1:nc),3);
    % [ACFaplog, ~, ~, ~]=FCS_imgdata(Ntotap,dt,0,Nlog);
    
     clearvars -except X nc minseg nseg F dt Lseg Tbin t0 T filter filtshape ACFlog ACF1log ACFaplog filename tau ks b taulog
    %h = waitbar(0,'processing data...');
    for i=minseg+1:nseg
        fprintf('\n');
        fprintf(strcat('Processing... ',num2str(i),'/',num2str(nseg)));
    [count, ~, ~, ~] = histcn( F,dt.*(Lseg*(i-1):Lseg*(i)),0:16:4096 );
    A=zeros(1);
    A(1,1:Lseg,1:256)=count(1:Lseg,1:256);
    clear count;
    
    A=double(A(:,:,t0+1:t0+T));
    % Ag=A(:,:,Tg:T);
    Ntot=sum(A,3);
    % Ng=sum(Ag,3);
    
    Nlog=256;
    [ACFtotlog, taulog, ~, ~]=FCS_imgdata(Ntot,dt,0,Nlog);
    ACFlog=ACFlog+ACFtotlog;
    % [ACFgatedlog, taulog, ~, ~]=FCS_imgdata(Ng,dt,0,Nlog);
    % ACFglog=ACFglog+ACFgatedlog;
    
        for k=1:nc
    
    Ns(:,:,k)=sum(filter(:,:,:,k).*A,3);
    [temp, taulog, ~, ~]=FCS_imgdata(Ns(:,:,k),dt,0,Nlog);
    ACF1log(k,:)=ACF1log(k,:)+ temp;
        end
    end
    
     clearvars -except X T minseg nseg taulog filtshape ACFlog ACF1log ACFaplog dt filename tau ks b
     
    fprintf('\n\n')
    fprintf('Done\n')
    
    ACFlog=ACFlog/(nseg+1-minseg);
    ACF1log=ACF1log/(nseg+1-minseg);
    
    
    figure
    subplot(2,2,2)
    plot(1:T,filtshape(:,1),1:T,filtshape(:,2),'--');
    axis([1 T -1 3]);
    
    subplot(2,2,1)
    semilogx(taulog, squeeze(ACFlog),'--');
    axis([dt dt*X/2 -0.0003 0.18]);
    
    subplot(2,2,3)
    semilogx(taulog, squeeze(ACF1log(1,:)));
    axis([dt dt*X/2 -0.0003 0.18]);
    
    subplot(2,2,4)
    semilogx(taulog, squeeze(ACF1log(2,:)));
    axis([dt dt*X/2 -0.0003 0.18]);
    
    ACFout=cat(2, taulog' , ACF1log(1,:)');
    
    dlmwrite([filename,'_ACF_ks',num2str(ks),'_tau',num2str(tau),'_b',num2str(b),'_ns',num2str(nseg),'_dt',num2str(dt*1e6), '.txt'],ACFout,'delimiter',';','precision',4);
    
