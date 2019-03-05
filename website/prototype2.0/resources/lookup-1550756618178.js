(function(window, undefined) {
  var dictionary = {
    "aafb2cbb-504f-4a30-8dae-0e3f0356aea1": "result 2 of search bar",
    "624f7c95-5f4c-4f66-b576-04e3dbb578a8": "Department profile",
    "b4f47ab7-49e2-4bb3-bcd3-5f5206f0dff4": "Search result - alternative2",
    "a0ff5884-f8ef-4586-887a-5105911f1765": "Search result - alternative1",
    "9ba93c87-54da-4821-8ac7-c0adcac791c0": "Programme profile",
    "0d4a11ad-f009-4179-8baf-dc76dea57264": "Search result",
    "a28e0964-90ca-4186-a23c-c7499dc919f3": "Main",
    "345ba5e5-188b-494b-81f9-38955a778d65": "result 1 of search bar",
    "798b60e3-197c-4449-a9b6-f63f22091796": "Search result - uni",
    "2f5b90eb-2181-4483-a896-4f396da6d2c4": "Main-interactivity",
    "82846413-e0c5-4d55-abed-b7bf843dd9f0": "Main-alternative",
    "105f21f3-df69-40ef-8dba-19592dd61e8e": "University pofile",
    "e73b655d-d3ec-4dcc-a55c-6e0293422bde": "960 grid - 16 columns",
    "ef07b413-721c-418e-81b1-33a7ed533245": "960 grid - 12 columns",
    "5b86e2de-2509-44d8-bff6-61c204a8d8c6": "Template 2",
    "f39803f7-df02-4169-93eb-7547fb8c961a": "Template 1",
    "bb8abf58-f55e-472d-af05-a7d1bb0cc014": "default"
  };

  var uriRE = /^(\/#)?(screens|templates|masters|scenarios)\/(.*)(\.html)?/;
  window.lookUpURL = function(fragment) {
    var matches = uriRE.exec(fragment || "") || [],
        folder = matches[2] || "",
        canvas = matches[3] || "",
        name, url;
    if(dictionary.hasOwnProperty(canvas)) { /* search by name */
      url = folder + "/" + canvas;
    }
    return url;
  };

  window.lookUpName = function(fragment) {
    var matches = uriRE.exec(fragment || "") || [],
        folder = matches[2] || "",
        canvas = matches[3] || "",
        name, canvasName;
    if(dictionary.hasOwnProperty(canvas)) { /* search by name */
      canvasName = dictionary[canvas];
    }
    return canvasName;
  };
})(window);