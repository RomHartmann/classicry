$( document ).bind( "pagebeforeshow", function() {
    
    $.mobile.loader.prototype.options.disabled = true;
    
    //values returned from backend
    lsCries = ['hungry', 'burp', 'discomfort', 'gas', 'sleepy']
    liConfidence = [16.97, 2.6, -3.67, -7.52, -8.38]
    
    lsCries = ['hungry', 'gas', 'sleepy', 'discomfort', 'burp']
    liConfidence = [27.18, 12.76, -1.05, -17.98, -20.93]
    
    
    
    
    //set colourscheme depending on cry's condidence
    lsColors = []
    iMin = common.min(liConfidence)
    iMax = common.max(liConfidence)
    liConfidence.forEach(function(iConf) {
        dColors = common.colour_scheme(iConf, iMax, iMin)
        iRed = Math.floor(dColors['iRed']*255);
        iBlue = Math.floor(dColors['iGreen']*255);
        iGreen = Math.floor(dColors['iBlue']*255);
        lsColors.push('rgba('+iRed+','+iBlue+','+iGreen+', 0.75)')
    })
    
    
    
    
    //initialize record functionality
//     var oSource = audio_context.createMediaStreamSource(stream);
//     var oRec = new Recorder(oSource);

    
    
    table_handlebars(lsCries)
    event_initialisations()
    
})




var event_initialisations = function() {
    
    $("#record").on('click', function() {
        common.showAlert('Recording 5 seconds at 8khz');
    })
    
    $("#stop_record").on('click', function() {
        common.showAlert('just for testing, stop recording and play sound');
    })
    
    
    $("#options").on('click', function() {
        common.options_in();
    })
    
    $(".cry_row").on('click', function() {
        
        //TODO remove and make general
        var sType = 'Hungry';
        var iConf = 27.18;
        details_handlebars(sType, iConf)
        
        common.details_in();
    })
    
    $("#overlay").on('click', function() {
        common.details_out();
        common.options_out();
    })
    
    $(window).on('swipeleft', function() {
        common.details_out();
    })
    
}




var table_handlebars = function(lsCries) {
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
    
}


var details_handlebars = function(sType, iConf) {
    //handlebars for table content's details
    
    sStats = "\
        This should all go in a help window or something:  \
        The mean confidence for all cries equals to zero, where high positive numbers \
        strongly favour the returned outcome, while large negative numbers disfavour \
        that outcome.\
        This should be dymaically generated:  \
        For example, "+iConf+" is a high value, and so strongly suggests that your baby \
        is "+sType+".\
    "
    sTips = ("\
        When your baby is hungry, you should probably feed it.  I recommend something \
        tasty like a McDonalds burger;  It is a fully balanced diet, since it contains \
        vegetables, meat, starch and oils.  Everything a newborn baby craves.\
    ")
    
    var ldContext = {
        sType: sType, 
        sStats: sStats,
        sTips: sTips
    }
    
    var sSource = $("#interp_details_handlebars").html();
    var oTemplate = Handlebars.compile(sSource); 
    var sHTML = oTemplate(ldContext)
    
    $('#interp_details_text').html(sHTML)
    
}






















