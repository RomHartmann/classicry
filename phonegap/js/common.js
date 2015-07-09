window.common = {}


common.keys = function(d) {
    //gets the dictionary keys as a list
    var l = [];
    for (var x in d) {
        l.push(x);
    }
    return l
}


common.values = function(d) {
    //gets the dictionary values as a list
    var l = [];
    for (var x in d) {
        l.push(d[x])
    }
    return l
}

common.min = function(l) {
    return Math.min.apply(null, l);
}

common.max = function(l) {
    return Math.max.apply(null, l);
}

common.sum = function(l) {
    //return sum of list
    iSum = 0;
    for (var i=0; i<l.length; i++) {
        iSum += l[i];
    }
    return iSum;
}


common.colour_scheme = function(iVal, iMax, iMin) {
    //creates the colorsheme based on confidence levels
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


common.showAlert = function(message, title) {
    //Uses the phones native alert system if possible
    if (navigator.notification) {
        navigator.notification.alert(message, null, title, 'OK');
    } else {
        alert(title ? (title + ": " + message) : message);
    }
}


common.details_in = function() {
    //animate the interpretation details in 
    $("#interp_details_window").animate({
        left: '10%'
    }, 200);
    $("#overlay").fadeIn(200)
}


common.details_out = function() {
    //animate the interpretation details out 
    $("#interp_details_window").animate({
        left: '-100%'
    }, 100);
    $("#overlay").fadeOut(100)
}



common.options_in = function() {
    //animate the options menu in 
    $("#options_menu").animate({
        width: '50%',
        height: '50%',
        top: '40px'
    }, 200);
    $("#overlay").fadeIn(200)
}


common.options_out = function() {
    //animate the options menu out 
    $("#options_menu").animate({
        width: '0%',
        height: '0%',
        top: '10px'
    }, 100);
    $("#overlay").fadeOut(100)
}





















