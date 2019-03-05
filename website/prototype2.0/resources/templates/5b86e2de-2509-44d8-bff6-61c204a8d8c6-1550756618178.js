jQuery("#simulation")
  .on("click", ".t-5b86e2de-2509-44d8-bff6-61c204a8d8c6 .click", function(event, data) {
    var jEvent, jFirer, cases;
    if(data === undefined) { data = event; }
    jEvent = jimEvent(event);
    jFirer = jEvent.getEventFirer();
    if(jFirer.is("#t-Rectangle_11")) {
      cases = [
        {
          "blocks": [
            {
              "actions": [
                {
                  "action": "jimNavigation",
                  "parameter": {
                    "target": "screens/345ba5e5-188b-494b-81f9-38955a778d65"
                  },
                  "exectype": "serial",
                  "delay": 0
                }
              ]
            }
          ],
          "exectype": "serial",
          "delay": 0
        }
      ];
      event.data = data;
      jEvent.launchCases(cases);
    }
  })
  .on("mouseup", ".t-5b86e2de-2509-44d8-bff6-61c204a8d8c6 .mouseup", function(event, data) {
    var jEvent, jFirer, cases;
    if(data === undefined) { data = event; }
    jEvent = jimEvent(event);
    jFirer = jEvent.getEventFirer();
    if(jFirer.is("#t-Rectangle_11")) {
      cases = [
        {
          "blocks": [
            {
              "actions": [
                {
                  "action": "jimChangeStyle",
                  "parameter": [ {
                    "#t-5b86e2de-2509-44d8-bff6-61c204a8d8c6 #t-Rectangle_11 > .backgroundLayer": {
                      "attributes": {
                        "background-color": "#282828"
                      }
                    }
                  },{
                    "#t-5b86e2de-2509-44d8-bff6-61c204a8d8c6 #t-Rectangle_11": {
                      "attributes-ie": {
                        "-pie-background": "#282828",
                        "-pie-poll": "false"
                      }
                    }
                  } ],
                  "exectype": "serial",
                  "delay": 0
                }
              ]
            }
          ],
          "exectype": "serial",
          "delay": 0
        }
      ];
      event.data = data;
      jEvent.launchCases(cases);
    }
  })
  .on("mousedown", ".t-5b86e2de-2509-44d8-bff6-61c204a8d8c6 .mousedown", function(event, data) {
    var jEvent, jFirer, cases;
    if(data === undefined) { data = event; }
    jEvent = jimEvent(event);
    jFirer = jEvent.getEventFirer();
    if(jFirer.is("#t-Rectangle_11")) {
      cases = [
        {
          "blocks": [
            {
              "actions": [
                {
                  "action": "jimChangeStyle",
                  "parameter": [ {
                    "#t-5b86e2de-2509-44d8-bff6-61c204a8d8c6 #t-Rectangle_11 > .backgroundLayer": {
                      "attributes": {
                        "background-color": "#999999"
                      }
                    }
                  },{
                    "#t-5b86e2de-2509-44d8-bff6-61c204a8d8c6 #t-Rectangle_11": {
                      "attributes-ie": {
                        "-pie-background": "#999999",
                        "-pie-poll": "false"
                      }
                    }
                  } ],
                  "exectype": "serial",
                  "delay": 0
                }
              ]
            }
          ],
          "exectype": "serial",
          "delay": 0
        }
      ];
      event.data = data;
      jEvent.launchCases(cases);
    }
  })
  .on("mouseenter dragenter", ".t-5b86e2de-2509-44d8-bff6-61c204a8d8c6 .mouseenter", function(event, data) {
    var jEvent, jFirer, cases;
    if(data === undefined) { data = event; }
    jEvent = jimEvent(event);
    jFirer = jEvent.getDirectEventFirer(this);
    if(jFirer.is("#t-Rectangle_11") && jFirer.has(event.relatedTarget).length === 0) {
      event.backupState = true;
      event.target = jFirer;
      cases = [
        {
          "blocks": [
            {
              "actions": [
                {
                  "action": "jimChangeStyle",
                  "parameter": [ {
                    "#t-5b86e2de-2509-44d8-bff6-61c204a8d8c6 #t-Rectangle_11 > .backgroundLayer": {
                      "attributes": {
                        "background-color": "#999999",
                        "background-attachment": "scroll"
                      }
                    }
                  },{
                    "#t-5b86e2de-2509-44d8-bff6-61c204a8d8c6 #t-Rectangle_11": {
                      "attributes-ie": {
                        "-pie-background": "#999999",
                        "-pie-poll": "false"
                      }
                    }
                  } ],
                  "exectype": "serial",
                  "delay": 0
                }
              ]
            }
          ],
          "exectype": "serial",
          "delay": 0
        }
      ];
      jEvent.launchCases(cases);
    }
  })
  .on("mouseleave dragleave", ".t-5b86e2de-2509-44d8-bff6-61c204a8d8c6 .mouseleave", function(event, data) {
    var jEvent, jFirer, cases;
    if(data === undefined) { data = event; }
    jEvent = jimEvent(event);
    jFirer = jEvent.getDirectEventFirer(this);
    if(jFirer.is("#t-Rectangle_11")) {
      jEvent.undoCases(jFirer);
    }
  });