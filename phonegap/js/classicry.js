$(document).ready(function () {
    
    $("#record").on('click', function() {
        alert('Recording 5 seconds at 8khz')
    })
    
    //values returned from backend
    lsCries = []
    liConfidence = []
    for (var i=0; i<5; i++) {
        lsCries.push('Cry '+ (i+1))
        liConfidence.push(10 - (5*i))
    }
    
    //set colourscheme depending on cry's condidence
    lsColors = []
    iMin = min(liConfidence)
    iMax = max(liConfidence)
    liConfidence.forEach(function(iConf) {
        dColors = colour_scheme(iConf, iMax, iMin)
        iRed = Math.floor(dColors['iRed']*255);
        iBlue = Math.floor(dColors['iGreen']*255);
        iGreen = Math.floor(dColors['iBlue']*255);
        lsColors.push('rgb('+iRed+','+iBlue+','+iGreen+')')
    })
    
    
    
    
    //handlebars for table
    var ldContext = [];
    for (var i=0; i<lsCries.length; i++) {
        
        sCry = lsCries[i]
        sConfidence = liConfidence[i]
        sColor = lsColors[i];
        
        ldContext.push({
            sCry: sCry, 
            sConfidence: sConfidence,
            sColor: sColor
        })
    }
    
    var sSource = $("#interp_list_handlebars").html(); 
    var oTemplate = Handlebars.compile(sSource); 
    var sHTML = oTemplate(ldContext)
    
    $('#results_table').html(sHTML)
    
    
    
    
    
})





var keys = function(d) {
    //gets the dictionary keys as a list
    var l = [];
    for (var x in d) {
        l.push(x);
    }
    return l
}


var values = function(d) {
    //gets the dictionary values as a list
    var l = [];
    for (var x in d) {
        l.push(d[x])
    }
    return l
}

var min = function(l) {
    return Math.min.apply(null, l);
}

var max = function(l) {
    return Math.max.apply(null, l);
}

var sum = function(l) {
    iSum = 0;
    for (var i=0; i<l.length; i++) {
        iSum += l[i];
    }
    return iSum;
}


var colour_scheme = function(iVal, iMax, iMin) {
    var iRed = 0;
    var iGreen = 0;
    var iBlue = 0;
    
    var iMaxNorm = iVal/iMax;
    var iMinNorm = iVal/iMin;
    
    if (iVal>=iMin && iVal<0){
        iRed = iMinNorm;
        iGreen = 0;
        iBlue = 1 - iMinNorm;
    }
    if (iVal>=0 && iVal<=iMax){
        iRed = 0;
        iGreen = iMaxNorm;
        iBlue = 1 - iMaxNorm;
    }
    
    dRet = {
        'iRed': iRed, 
        'iGreen': iGreen, 
        'iBlue': iBlue
    }
    
    return dRet;
}













