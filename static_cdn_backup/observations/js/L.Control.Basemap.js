L.Control.Basemaps = L.Control.extend({
    _map: null,
    includes: L.Evented ? L.Evented.prototype : L.Mixin.Event,
    options: {
        position: "bottomright",
        tileX: 0,
        tileY: 0,
        tileZ: 0,
        layers: []
    },
    basemap: null,
    onAdd: function (e) {
        this._map = e;
        var t = L.DomUtil.create("div", "basemaps leaflet-control closed");
        return L.DomEvent.disableClickPropagation(t), L.Browser.touch || L.DomEvent.disableScrollPropagation(t), this.options.basemaps.forEach(function (s, o) {
            var a, i = "basemap";
            if (0 === o ? (this.basemap = s, this._map.addLayer(s), i += " active") : 1 === o && (i += " alt"), s.options.iconURL) a = s.options.iconURL;
            else {
                var l = {
                    x: this.options.tileX,
                    y: this.options.tileY
                };
                if (a = L.Util.template(s._url, L.extend({
                        s: s._getSubdomain(l),
                        x: l.x,
                        y: s.options.tms ? s._globalTileRange.max.y - l.y : l.y,
                        z: this.options.tileZ
                    }, s.options)), s instanceof L.TileLayer.WMS) {
                    s._map = e;
                    var n = s.options.crs || e.options.crs,
                        r = L.extend({}, s.wmsParams),
                        m = parseFloat(r.version);
                    r[m >= 1.3 ? "crs" : "srs"] = n.code;
                    var p = L.point(l);
                    p.z = this.options.tileZ;
                    var c = s._tileCoordsToBounds(p),
                        d = n.project(c.getNorthWest()),
                        h = n.project(c.getSouthEast()),
                        v = (m >= 1.3 && n === L.CRS.EPSG4326 ? [h.y, d.x, d.y, h.x] : [d.x, h.y, h.x, d.y]).join(",");
                    a += L.Util.getParamString(r, a, s.options.uppercase) + (s.options.uppercase ? "&BBOX=" : "&bbox=") + v
                }
            }
            var b = L.DomUtil.create("div", i, t),
                u = L.DomUtil.create("img", null, b);
            u.src = a, s.options && s.options.label && (u.title = s.options.label), L.DomEvent.on(b, "click", function () {
                if (this.options.basemaps.length > 2 && L.Browser.mobile && L.DomUtil.hasClass(t, "closed")) L.DomUtil.removeClass(t, "closed");
                else if (s != this.basemap) {
                    e.removeLayer(this.basemap), e.addLayer(s), s.bringToBack(), e.fire("baselayerchange", s), this.basemap = s, L.DomUtil.removeClass(t.getElementsByClassName("basemap active")[0], "active"), L.DomUtil.addClass(b, "active");
                    var a = (o + 1) % this.options.basemaps.length;
                    L.DomUtil.removeClass(t.getElementsByClassName("basemap alt")[0], "alt"), L.DomUtil.addClass(t.getElementsByClassName("basemap")[a], "alt"), L.DomUtil.addClass(t, "closed")
                }
            }, this)
        }, this), this.options.basemaps.length > 2 && !L.Browser.mobile && (L.DomEvent.on(t, "mouseenter", function () {
            L.DomUtil.removeClass(t, "closed")
        }, this), L.DomEvent.on(t, "mouseleave", function () {
            L.DomUtil.addClass(t, "closed")
        }, this)), this._container = t, this._container
    }
}), L.control.basemaps = function (e) {
    return new L.Control.Basemaps(e)
};