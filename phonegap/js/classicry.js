$(document).ready(function () {
    
    
    
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

    
    
    create_handlebars()
    button_presses()
    
})





var button_presses = function() {
    
    $("#record").on('click', function() {
        common.showAlert('Recording 5 seconds at 8khz')
    })
    
    $("#stop_record").on('click', function() {
        alert('Stahp')
    })
    
    
    $("#options").on('click', function() {
        alert('This should open options:  help, buy app, font, background, record length')
    })
    
    $(".cry_row").on('click', function() {
//         alert('this should bring up a window with info, help and advice on said cry\
//         burp: eh\
//         discomfort: heh\
//         gas: eair\
//         hungry: neh\
//         sleepy: owh')
    })
}




var create_handlebars = function() {
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

























