(function ($) {
  "use strict";

  // Matches the deterministic Django admin URL pattern for this app:
  // <admin-prefix>/<app_label>/<model_name>/<custom-path>/
  var REGIONS_URL_BASE = "/minhalah/api/branch/regions-for-country/";

  function loadRegions(countryId, selectedRegionId) {
    var $region = $("#id_region");
    if (!$region.length) return;

    $region.empty().append($("<option></option>").val("").text("---------"));

    if (!countryId) return;

    $.getJSON(REGIONS_URL_BASE + countryId + "/", function (data) {
      data.forEach(function (region) {
        var $opt = $("<option></option>").val(region.id).text(region.name);
        if (selectedRegionId && String(region.id) === String(selectedRegionId)) {
          $opt.prop("selected", true);
        }
        $region.append($opt);
      });
    });
  }

  $(function () {
    var $country = $("#id_country");
    if (!$country.length) return;

    var initialRegionId = $("#id_region").val();
    if ($country.val()) {
      loadRegions($country.val(), initialRegionId);
    }

    $country.on("change", function () {
      loadRegions($(this).val(), null);
    });
  });
})(window.jQuery || (window.django && window.django.jQuery));
