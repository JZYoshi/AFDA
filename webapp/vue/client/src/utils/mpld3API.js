const $mpld3 = new (function MPL3D() {
  this.wait_for_mpld3 = (callback, ...args) => {
    if (window.mpld3) {
      callback(...args);
    } else {
      setTimeout(() => {
        this.wait_for_mpld3(callback, ...args);
      }, 500);
    }
  };

  this.draw_figure = (figid, spec) => {
    if (!window.mpld3) {
      this.wait_for_mpld3(this.draw_figure, figid, spec);
    } else {
      window.mpld3.draw_figure(figid, spec, null, true);
    }
  };
})();

export default $mpld3;
