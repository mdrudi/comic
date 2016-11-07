#!/bin/bash
# questo script lavora direttamente sulle medie mensili originali

# LISTA DIRECTORIES IN USO
InDir=/data/oliveri/Melodies-Conversion/Input
WorkDir=/data/oliveri/Melodies-Conversion/Codice-Manipolazione
MaskDir=/data/oliveri/Melodies-Conversion/File-Maschera
OutDir=/data/oliveri/Melodies-Conversion/Output

# CARICAMENTO FILE NELLA CARTELLA WORKDIR
export WorkDir PATH=$PATH:$WorkDir

# IMPOSTAZIONE VARIABILI E ATTRIBUTI GLOBALI
SetGlobalForecast() {

    if [ $Type == "f" ]; then
    	 Cmd="ncatted -h -a bulletin_type,global,o,c,\"forecast\" $1"
    	 echo $Cmd
    	 eval $Cmd
    fi
    if [ $Type == "s" ]; then
     	 Cmd="ncatted -h -a bulletin_type,global,o,c,\"simulation\" $1"
    	 echo $Cmd
    	 eval $Cmd
    fi
    if [ $Type == "a" ]; then
    	 Cmd="ncatted -h -a bulletin_type,global,o,c,\"analysis\" $1"
    	 echo $Cmd
    	 eval $Cmd
    fi
    if [ $Type == "r" ]; then
    	 Cmd="ncatted -h -a bulletin_type,global,o,c,\"reanalysis\" $1"
    	 echo $Cmd
    	 eval $Cmd
    fi
    Cmd="ncatted -h -a institution,global,o,c,\"Istituto Nazionale di Geofisica e Vulcanologia -  Bologna, Italy\" $1"
    echo $Cmd
    eval $Cmd
    # Cmd="ncatted -h -a source,global,o,c,\"SOURCE TEXT\" $1"
    # echo $Cmd
    # eval $Cmd
    # Cmd="ncatted -h -a contact,global,o,c,\"CONTACT TEXT\" $1"
    # echo $Cmd
    # eval $Cmd
    # Cmd="ncatted -h -a references,global,o,c,\"REFERENCES TEXT\" $1"
    # echo $Cmd
    # eval $Cmd
    # Cmd="ncatted -h -a comment,global,o,c,\"COMMENT TEXT\" $1"
    # echo $Cmd
    # eval $Cmd
    Cmd="ncatted -h -O -a field_type,global,o,c,\"monthly_mean_beginning_from_time_field\" $1 "
    echo $Cmd
    eval $Cmd
    sgfYYYY=`echo ${CycleDate}| cut -c1-4`
    sgfMM=`echo ${CycleDate}| cut -c5-6`
    # Cmd="ncatted -h -a Date,global,o,c,\"${sgfYYYY} ${sgfMM}\" $1"
    # echo $Cmd
    # eval $Cmd
    Date=$(LC_ALL=en.US.utf8 date -u)
    Cmd="ncatted -h -a history,global,o,c,\"Converted From NEXTDATA Format $Date\" $1"
    echo $Cmd
    eval $Cmd
    Cmd="ncatted -h -a Conventions,global,o,c,\"CF-1.6\" $1"
    echo $Cmd
    eval $Cmd

}


# IMPOSTAZIONE DIMENSIONI VARIABILI
SetSpecificForecast(){

    echo
    echo RIDENOMINAZIONE DIMENSIONI
    # RIDENOMINAZIONE DIMENSIONI
    Cmd="ncrename -O -d x,lon -d y,lat -d time_counter,time $1"
    echo $Cmd
    eval $Cmd
    if [ $GridMR = "T" ]; then 
        Cmd="ncrename -O -d deptht,depth $1"
    elif [ $GridMR = "U" ]; then 
        Cmd="ncrename -O -d depthu,depth $1"
    elif [ $GridMR = "V" ]; then 
	Cmd="ncrename -O -d depthv,depth $1"
    fi
    echo $Cmd
    eval $Cmd
    echo
    echo APPENDE LATITUDINE E LONGITUDINE
    # APPENDE LATITUDINE E LONGITUDINE
    Cmd="ncks -O -x -v nav_lon,nav_lat,time_counter $1 $1"
    echo $Cmd
    eval $Cmd
    if [ $GridMR = "T" ]; then 
        Cmd="ncks -h -A $MaskDir/gridmaskT3D_sys4a3.nc $1"
    elif [ $GridMR = "U" ]; then 
        Cmd="ncks -h -A $MaskDir/gridmaskU3D_sys5.nc $1"
    elif [ $GridMR = "V" ]; then 
	Cmd="ncks -h -A $MaskDir/gridmaskV3D_sys5.nc $1"
    fi
    echo $Cmd
    eval $Cmd
    echo
    echo APPENDE IL TEMPO
    # APPENDE IL TEMPO
    FirstDate=`jday.py $DestDate -1`
    TimeDate=$FirstDate
    LastDate=`jday.py $(jmonth.py $CycleDate +1)01 -1`
    Cmd="time_counter_bnds_1953.sh $FirstDate $TimeDate $LastDate | ncgen -o time_counter_bnds.nc"
    echo $Cmd
    eval $Cmd
    Cmd="ncks -h -A time_counter_bnds.nc $1"
    echo $Cmd
    eval $Cmd
    Cmd="rm -f time_counter_bnds.nc"
    echo $Cmd
    eval $Cmd
}


# FUNZIONE CALCOLO MIN VARIABILI
ncVarMin() {
    
    # Argomenti funzione: 
    # $1 = nome file
    # $2 = nome variabile
    Cmd="ncap2 -h -O -C -v -s 'min=${2}.min();print(min)' $1 tmp_min.nc | cut -d' ' -f3"
    eval $Cmd
    
}


# FUNZIONE CALCOLO MAX VARIABILI
ncVarMax() {
    
    # Argomenti funzione: 
    # $1 = nome file
    # $2 = nome variabile
    # $3 = Fill Value
    # $4 = Valore Minimo della variabile da sostituire al FillValue prima di eseguire il massimo
    Cmd="ncap2 -h -O -C -v -s 'where($2>$3/10) $2=$4; max=$2.max();print(max)' $1 tmp_max.nc | cut -d' ' -f3"
    eval $Cmd
}


# IMPOSTAZIONE ATTRIBUTI LOCALI VARIABILI
SetAttrib() {
    
    # Argomenti funzione: 
    # $1 = nome file
    # $2 = nome variabile
    # $3 = units
    # $4 = standard name
    # $5 = long name
    echo
    echo IMPOSTAZIONE ATTRIBUTI $2
    Cmd="ncatted -a short_name,$2,d,, -a interval_operation,$2,d,, -a interval_write,$2,d,, $1"
    echo $Cmd
    eval $Cmd
    Cmd="ncatted -a associate,$2,d,, -a online_operation,$2,d,, $1"
    echo $Cmd
    eval $Cmd
    Cmd="ncatted -a valid_min,$2,d,, -a valid_max,$2,d,, $1"
    echo $Cmd
    eval $Cmd
    VarMin=$(ncVarMin $1 $2)
    VarMax=$(ncVarMax $1 $2 1.e+20 $VarMin)
    Cmd="ncatted -a valid_min,$2,c,d,$VarMin -a valid_max,$2,c,d,$VarMax $1"
    echo $Cmd
    eval $Cmd
    Cmd="ncatted -a _FillValue,$2,o,f,1.e20 $1"
    echo $Cmd
    eval $Cmd
    Cmd="ncatted -a missing_value,$2,o,f,1.e20 $1"
    echo $Cmd
    eval $Cmd
    Cmd="ncatted -a axis,$2,d,, $1" 
    echo $Cmd
    eval $Cmd
    Cmd="ncatted -a units,$2,o,c,$3 $1"
    echo $Cmd
    eval $Cmd   
    if  [ $2 = "sossheig" ] || [ $2 = "sowaflup" ] || [ $2 = "sohefldo" ] || [ $2 = "soshfldo" ] || [ $2 = "sozotaux" ]  || [ $2 = "sometauy" ]; then 
        Cmd="ncatted -a coordinates,$2,o,c,\"time lat lon\" $1"
        echo $Cmd
        eval $Cmd
    else
        Cmd="ncatted -a coordinates,$2,o,c,\"time depth lat lon\" $1"
        echo $Cmd
        eval $Cmd
    fi
    Cmd="ncatted -a standard_name,$2,o,c,$4 $1"
    echo $Cmd
    eval $Cmd
    Cmd="ncatted -a long_name,$2,o,c,\"$5\" $1"
    echo $Cmd
    eval $Cmd
    
}

#DEFINIZIONE NOME FILE DI OUTPUT
OutFileName() {

    Type=`basename $1| cut -d _ -f 3`
    if [ $Type == "f" ] ; then ofn_fctype="fc" ; fi 
    if [ $Type == "a" ] ; then ofn_fctype="an" ; fi 
    if [ $Type == "s" ] ; then ofn_fctype="sm" ; fi 
    if [ $Type == "r" ] ; then ofn_fctype="re" ; fi 
    ofn_file_name=`basename $1`
    ofn_production_data_str="MELODIES_$ofn_fctype"
    ofn_ptype=$2
    ofn_file_name_data=`echo $ofn_file_name | cut -c-6`
    ofn_str1="_mm-INGV--${ofn_ptype}-MED-"
    ofn_str2=".nc"
    ofn_out_file_name=${ofn_file_name_data}${ofn_str1}${ofn_production_data_str}${ofn_str2} 
    echo $ofn_out_file_name

}


# FUNZIONE DI PROCESSAMENTO PRINCIPALE
ProcessOneFile() {
																				
    echo '+--------------------------------------------------------------------------------------+'
    echo '|               ProcessOneFile:GridMR= '$GridMR 'DestDate= '$DestDate 'Type= '$Type '                   |'
    echo '|								        	       |'

    echo
    # TAGLIO ZONA ATLANTICA
    echo TAGLIO ZONA ATLANTICA
    Cmd="ncks -O -h -d x,194,870 -C $1 $1"
    echo $Cmd
    eval $Cmd
    echo
    # RIMOZIONE ATTRIBUTI GLOBALI PREESISTENTI
    echo RIMOZIONE ATTRIBUTI GLOBALI PREESISTENTI
    Cmd="ncatted -h -a ,global,d,, $1"
    echo $Cmd
    eval $Cmd
    echo
    # RIMOZIONE ATTRIBUTI LOCALI PREESISTENTI
    echo RIMOZIONE ATTRIBUTI LOCALI PREESISTENTI
    Cmd="ncatted -h -a ,,d,, $1"
    echo $Cmd
    eval $Cmd
    echo
    # SOVRASCRITTURA CON FILE DI MASCHERA
    echo SOVRASCRITTURA CON FILE DI MASCHERA
    Cmd="ncbo -h -O -y mlt $1 $MaskDir/template_mask_${GridMR}_f_D.nc $1"
    echo $Cmd
    eval $Cmd
    echo
    echo IMPOSTAZIONE DIMENSIONI VARIABILI
    SetSpecificForecast $1 $GridMR
    if [ $GridMR = "T" ]; then
        SetAttrib $1 "votemper" "C" "sea_water_potential_temperature" "Sea Water Potential Temperature"
        SetAttrib $1 "vosaline" "1e-3" "sea_water_salinity" "Sea Water Salinity"
        # SetAttrib $1 "sossheig" "m" "sea_surface_height" "sea surface height"
        # SetAttrib $1 "sowaflup" "Kg/m^2/s" "net_upward_water_flux" "Net Upward Water Flux"
        # SetAttrib $1 "sohefldo" "W/m^2" "net_downward_heat_flux" "Net Downward Heat Flux"
        # SetAttrib $1 "soshfldo" "W/m^2" "shortwave_radiation" "Shortwave Radiation"
    fi

    if [ $GridMR = "U" ]; then
        SetAttrib "$1" "vozocrtx" "m/s" "eastward_sea_water_velocity" "Sea Water Zonal Current"
        SetAttrib "$1" "sozotaux" "N/m2" "surface_downward_eastward_stress" "Wind Stress along i-axis"
    fi

    if [ $GridMR = "V" ]; then
        SetAttrib "$1" "vomecrty" "m/s" "northward_sea_water_velocity" "Sea Water Meridional Current"
        SetAttrib "$1" "sometauy" "N/m2" "surface_downward_northward_stress" "Wind Stress along j-axis"
    fi
    echo
    echo IMPOSTAZIONE VARIABILI E ATTRIBUTI GLOBALI
    SetGlobalForecast $1

}

# FILE PRINCIPALE
if [ ! -d $OutDir ] ; then
    echo
    echo CREAZIONE CARTELLA FILE DI OUTPUT
    Cmd="mkdir $OutDir"
    echo $Cmd
    eval $Cmd
fi
echo
echo RIMOZIONE FILE DI LAVORO PRECEDENTI RIMASTI
Cmd="cd $WorkDir ; rm -f *tmp.nc*"
echo $Cmd
eval $Cmd
for InFile in `ls -1 $InDir/*_[T-V].nc.gz` ; do
    Type=r
    GridMR=`basename $InFile  | cut -d_ -f2 |cut -c1`
    CycleDate=`basename $InFile  | cut -d_ -f1`
    # OPZIONE MESI
    DestDate=${CycleDate}01
    WorkFile=${CycleDate}_${GridMR}_${Type}_tmp.nc.gz
    echo
    echo PROCESSAMENTO FILE $WorkFile
    echo
    Cmd="cp $InFile $WorkFile"
    echo $Cmd
    eval $Cmd
    Cmd="gunzip $WorkFile"
    echo $Cmd
    eval $Cmd
    echo
    WorkFile=`basename $WorkFile | rev | cut -c 4- | rev`
    ProcessOneFile $WorkFile
done
Cmd="rm -f tmp_min.nc tmp_max.nc"
echo $Cmd
eval $Cmd
firstDate=`ls -1 *tmp.nc |head -1| cut -d_ -f1 `
echo
echo PRIMA DATA: mese $(echo $firstDate |cut -c5-6) anno $(echo $firstDate |cut -c1-4)
lastDate=`ls -1 *tmp.nc  |tail -1| cut -d_ -f1 `
echo
echo ULTIMA DATA: mese $(echo $lastDate |cut -c5-6) anno $(echo $lastDate |cut -c1-4)
idate=$firstDate
# impongo il valore di CycleDate (valore che finisce nella date del nomefile)
while [ $idate -le $lastDate ] ; do
    Month=$(echo $idate |cut -c5-6)
    Year=$(echo $idate |cut -c1-4)
    echo
    echo SCRITTURA E COMPATTAMENTO FILE DI OUTPUT mese $Month anno $Year
    echo
    finfil=`ls -1 ${idate}_T_?_tmp.nc`
    if [ ! -z $finfil ]; then
        WorkFileT=`ls -1 ${idate}_T_?_tmp.nc`
        WorkFileU=`ls -1 ${idate}_U_?_tmp.nc`
        WorkFileV=`ls -1 ${idate}_V_?_tmp.nc`
	TEMP_FileName=`OutFileName $WorkFileT TEMP`
        PSAL_FileName=`OutFileName $WorkFileT PSAL`
        UCUR_FileName=`OutFileName $WorkFileU UCUR`
        VCUR_FileName=`OutFileName $WorkFileV VCUR`
        TAUX_FileName=`OutFileName $WorkFileU TAUX`
        TAUY_FileName=`OutFileName $WorkFileV TAUY`
        # TEMP
	Cmd="ncks -O -h -v time_bnds $WorkFileT ${idate}_Ttmp.nc2"
        echo $Cmd
        eval $Cmd
        Cmd="ncks -A -h -v votemper $WorkFileT ${idate}_Ttmp.nc2"
	echo $Cmd
	eval $Cmd
        Cmd="ncatted -h -a title,global,o,c,\"Potential Temperature (3D) - Monthly Mean\" ${idate}_Ttmp.nc2"
        echo $Cmd
        eval $Cmd
        Cmd="ncatted -h -a NCO,global,d,, ${idate}_Ttmp.nc2 "
        echo $Cmd
        eval $Cmd
        cmd="gzip < ${idate}_Ttmp.nc2 > $OutDir/${TEMP_FileName}.gz"
        echo $cmd
        eval $cmd 
        # SALT
	Cmd="ncks -O -h -v time_bnds $WorkFileT ${idate}_Ttmp.nc2"
        echo $Cmd
        eval $Cmd
        Cmd="ncks -A -h -v vosaline $WorkFileT ${idate}_Ttmp.nc2"
        echo $Cmd
        eval $Cmd
        Cmd="ncatted -h -a title,global,o,c,\"Salinity (3D) - Monthly Mean\" ${idate}_Ttmp.nc2"
        echo $Cmd
        eval $Cmd
        Cmd="ncatted -h -a NCO,global,d,, ${idate}_Ttmp.nc2 "
        echo $Cmd
        eval $Cmd
        cmd="gzip < ${idate}_Ttmp.nc2 > $OutDir/${PSAL_FileName}.gz"
        echo $cmd
        eval $cmd 
        # # SSH
	# Cmd="ncks -O -h -v time_bnds $WorkFileT ${idate}_Ttmp.nc2"
        # echo $Cmd
        # eval $Cmd
        # Cmd="ncks -A -h -v sossheig $WorkFileT ${idate}_Ttmp.nc2"
	# echo $Cmd
        # eval $Cmd
        # Cmd="ncatted -h -a title,global,o,c,\"Sea Surface Height (2D) - Monthly Mean\" ${idate}_Ttmp.nc2"
        # echo $Cmd
        # eval $Cmd
        # Cmd="ncatted -h -a NCO,global,d,, ${idate}_Ttmp.nc2 "
        # echo $Cmd
        # eval $Cmd
        # cmd="gzip < ${idate}_Ttmp.nc2 > $OutDir/${T_FileName}.gz"
        # echo $cmd
        # eval $cmd
	# # NET UPWARD WATER FLUX
        # Cmd="ncks -O -h -v sowaflup $WorkFileT ${idate}_Ttmp.nc2"
        # echo $Cmd
        # eval $Cmd
	# Cmd="ncks -A -h -v time_bnds $WorkFileT ${idate}_Ttmp.nc2"
        # echo $Cmd
        # eval $Cmd
        # Cmd="ncatted -h -a title,global,o,c,\"Net Upward Water Flux (2D) - Monthly Mean\" ${idate}_Ttmp.nc2"
        # echo $Cmd
        # eval $Cmd
        # Cmd="ncatted -h -a NCO,global,d,, ${idate}_Ttmp.nc2 "
        # echo $Cmd
        # eval $Cmd
        # cmd="gzip < ${idate}_Ttmp.nc2 > $OutDir/${T_FileName}.gz"
        # echo $cmd
        # eval $cmd
        # # NET DOWNWARD HEAT FLUX
        # Cmd="ncks -O -h -v sohefldo $WorkFileT ${idate}_Ttmp.nc2"
        # echo $Cmd
        # eval $Cmd
	# Cmd="ncks -A -h -v time_bnds $WorkFileT ${idate}_Ttmp.nc2"
	# echo $Cmd
        # eval $Cmd
        # Cmd="ncatted -h -a title,global,o,c,\"Net Downward Heat Flux (2D) - Monthly Mean\" ${idate}_Ttmp.nc2"
        # echo $Cmd
        # eval $Cmd
        # Cmd="ncatted -h -a NCO,global,d,, ${idate}_Ttmp.nc2 "
        # echo $Cmd
        # eval $Cmd
        # cmd="gzip < ${idate}_Ttmp.nc2 > $OutDir/${T_FileName}.gz"
        # echo $cmd
        # eval $cmd
        # # SHORTWAVE RADIATION
	# Cmd="ncks -O -h -v soshfldo $WorkFileT ${idate}_Ttmp.nc2"
        # echo $Cmd
        # eval $Cmd
        # Cmd="ncks -A -h -v time_bnds $WorkFileT ${idate}_Ttmp.nc2"
        # echo $Cmd
        # eval $Cmd
        # Cmd="ncatted -h -a title,global,o,c,\"Shortwave Radiation (2D) - Monthly Mean\" ${idate}_Ttmp.nc2"
        # echo $Cmd
        # eval $Cmd
        # Cmd="ncatted -h -a NCO,global,d,, ${idate}_Ttmp.nc2 "
        # echo $Cmd
        # eval $Cmd
        # cmd="gzip < ${idate}_Ttmp.nc2 > $OutDir/${T_FileName}.gz"
        # echo $cmd
        # eval $cmd

        # RIMOZIONE FILE TEMPORANEO T
	Cmd="rm ${idate}_Ttmp.nc2 "
	echo $Cmd
        eval $Cmd
	
        # U
	Cmd="ncks -O -h -v time_bnds $WorkFileU ${idate}_Utmp.nc2"
        echo $Cmd
        eval $Cmd
        Cmd="ncks -A -h -v vozocrtx $WorkFileU ${idate}_Utmp.nc2"
	echo $Cmd
	eval $Cmd
        Cmd="ncatted -h -a title,global,o,c,\"Zonal Velocity (3D) - Monthly Mean\" ${idate}_Utmp.nc2"
        echo $Cmd
        eval $Cmd
        Cmd="ncatted -h -a NCO,global,d,, ${idate}_Utmp.nc2 "
        echo $Cmd
        eval $Cmd
        cmd="gzip < ${idate}_Utmp.nc2 > $OutDir/${UCUR_FileName}.gz"
        echo $cmd
        eval $cmd
        # TAUX
	Cmd="ncks -O -h -v time_bnds $WorkFileU ${idate}_Utmp.nc2"
        echo $Cmd
        eval $Cmd
        Cmd="ncks -A -h -v sozotaux $WorkFileU ${idate}_Utmp.nc2"
	echo $Cmd
        eval $Cmd
        Cmd="ncatted -h -a title,global,o,c,\"Zonal Wind Stress (2D) - Monthly Mean\" ${idate}_Utmp.nc2"
        echo $Cmd
        eval $Cmd
        Cmd="ncatted -h -a NCO,global,d,, ${idate}_Utmp.nc2 "
        echo $Cmd
        eval $Cmd
        cmd="gzip < ${idate}_Utmp.nc2 > $OutDir/${TAUX_FileName}.gz"
        echo $cmd
        eval $cmd

        # RIMOZIONE FILE TEMPORANEO U
	Cmd="rm ${idate}_Utmp.nc2 "
	echo $Cmd
        eval $Cmd

	# V
	Cmd="ncks -O -h -v time_bnds $WorkFileV ${idate}_Vtmp.nc2"
        echo $Cmd
        eval $Cmd
        Cmd="ncks -A -h -v vomecrty $WorkFileV ${idate}_Vtmp.nc2"
	echo $Cmd
	eval $Cmd
        Cmd="ncatted -h -a title,global,o,c,\"Meridional Velocity (3D) - Monthly Mean\" ${idate}_Vtmp.nc2"
        echo $Cmd
        eval $Cmd
        Cmd="ncatted -h -a NCO,global,d,, ${idate}_Vtmp.nc2 "
        echo $Cmd
        eval $Cmd
        cmd="gzip < ${idate}_Vtmp.nc2 > $OutDir/${VCUR_FileName}.gz"
        echo $cmd
        eval $cmd 
	# TAUY
	Cmd="ncks -O -h -v time_bnds $WorkFileV ${idate}_Vtmp.nc2"
        echo $Cmd
        eval $Cmd
        Cmd="ncks -A -h -v sometauy $WorkFileV ${idate}_Vtmp.nc2"
	echo $Cmd
	eval $Cmd
        Cmd="ncatted -h -a title,global,o,c,\"Meridional Wind Stress (2D) - Monthly Mean\" ${idate}_Vtmp.nc2"
        echo $Cmd
        eval $Cmd
        Cmd="ncatted -h -a NCO,global,d,, ${idate}_Vtmp.nc2 "
        echo $Cmd
        eval $Cmd
        cmd="gzip < ${idate}_Vtmp.nc2 > $OutDir/${TAUY_FileName}.gz"
        echo $cmd
        eval $cmd
	
        # RIMOZIONE FILE TEMPORANEO V
	Cmd="rm ${idate}_Vtmp.nc2 "
	echo $Cmd
        eval $Cmd

	# RIMOZIONE FILE DI LAVORO
        Cmd="rm -f $WorkFileT $WorkFileU $WorkFileV $WorkFileO"
        echo $Cmd
        eval $Cmd
    else
        echo non ci sono files ${idate}_[T-V]*
    fi #finfil non e' vuoto
    idate=`jmonth.py $idate +1`
done
echo
echo Finished!
