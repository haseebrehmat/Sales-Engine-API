/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, { enumerable: true, get: getter });
/******/ 		}
/******/ 	};
/******/
/******/ 	// define __esModule on exports
/******/ 	__webpack_require__.r = function(exports) {
/******/ 		if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 			Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 		}
/******/ 		Object.defineProperty(exports, '__esModule', { value: true });
/******/ 	};
/******/
/******/ 	// create a fake namespace object
/******/ 	// mode & 1: value is a module id, require it
/******/ 	// mode & 2: merge all properties of value into the ns
/******/ 	// mode & 4: return value when already ns object
/******/ 	// mode & 8|1: behave like require
/******/ 	__webpack_require__.t = function(value, mode) {
/******/ 		if(mode & 1) value = __webpack_require__(value);
/******/ 		if(mode & 8) return value;
/******/ 		if((mode & 4) && typeof value === 'object' && value && value.__esModule) return value;
/******/ 		var ns = Object.create(null);
/******/ 		__webpack_require__.r(ns);
/******/ 		Object.defineProperty(ns, 'default', { enumerable: true, value: value });
/******/ 		if(mode & 2 && typeof value != 'string') for(var key in value) __webpack_require__.d(ns, key, function(key) { return value[key]; }.bind(null, key));
/******/ 		return ns;
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "/";
/******/
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = 240);
/******/ })
/************************************************************************/
/******/ ([
/* 0 */,
/* 1 */,
/* 2 */
/***/ (function(module, exports, __webpack_require__) {

var global = __webpack_require__(3);
var core = __webpack_require__(18);
var hide = __webpack_require__(13);
var redefine = __webpack_require__(30);
var ctx = __webpack_require__(33);
var PROTOTYPE = 'prototype';

var $export = function (type, name, source) {
  var IS_FORCED = type & $export.F;
  var IS_GLOBAL = type & $export.G;
  var IS_STATIC = type & $export.S;
  var IS_PROTO = type & $export.P;
  var IS_BIND = type & $export.B;
  var target = IS_GLOBAL ? global : IS_STATIC ? global[name] || (global[name] = {}) : (global[name] || {})[PROTOTYPE];
  var exports = IS_GLOBAL ? core : core[name] || (core[name] = {});
  var expProto = exports[PROTOTYPE] || (exports[PROTOTYPE] = {});
  var key, own, out, exp;
  if (IS_GLOBAL) source = name;
  for (key in source) {
    // contains in native
    own = !IS_FORCED && target && target[key] !== undefined;
    // export native or passed
    out = (own ? target : source)[key];
    // bind timers to global for call from export context
    exp = IS_BIND && own ? ctx(out, global) : IS_PROTO && typeof out == 'function' ? ctx(Function.call, out) : out;
    // extend global
    if (target) redefine(target, key, out, type & $export.U);
    // export
    if (exports[key] != out) hide(exports, key, exp);
    if (IS_PROTO && expProto[key] != out) expProto[key] = out;
  }
};
global.core = core;
// type bitmap
$export.F = 1;   // forced
$export.G = 2;   // global
$export.S = 4;   // static
$export.P = 8;   // proto
$export.B = 16;  // bind
$export.W = 32;  // wrap
$export.U = 64;  // safe
$export.R = 128; // real proto method for `library`
module.exports = $export;


/***/ }),
/* 3 */
/***/ (function(module, exports) {

// https://github.com/zloirock/core-js/issues/86#issuecomment-115759028
var global = module.exports = typeof window != 'undefined' && window.Math == Math
  ? window : typeof self != 'undefined' && self.Math == Math ? self
  // eslint-disable-next-line no-new-func
  : Function('return this')();
if (typeof __g == 'number') __g = global; // eslint-disable-line no-undef


/***/ }),
/* 4 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "Target", function() { return Target; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "Type", function() { return Type; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "Namespace", function() { return Namespace; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "sendMessage", function() { return sendMessage; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "isTarget", function() { return isTarget; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "isType", function() { return isType; });
/*
  Utilities for sending/receiving messages within the PIA application

  @type Listener <T> = (payload: T) => void;
*/
const Target = {
  ALL: '@all',
  POPUPS: '@popups',
  FOREGROUND: '@foreground',
  BACKGROUND: '@background'
};
const Namespace = {
  REGIONLIST: 'util.regionlist',
  PROXY: 'proxy',
  BYPASSLIST: 'util.bypasslist',
  I18N: 'util.i18n'
};
const Type = {
  FOREGROUND_OPEN: 'foreground_open',
  UPDATE_PAC_INFO: 'update_pac_info',
  DEBUG: 'debug',
  SET_SELECTED_REGION: `${Namespace.REGIONLIST}.setSelectedRegion`,
  IMPORT_REGIONS: `${Namespace.REGIONLIST}.import`,
  IMPORT_AUTO_REGION: `${Namespace.REGIONLIST}.setAutoRegion`,
  SET_FAVORITE_REGION: `${Namespace.REGIONLIST}.setFavoriteRegion`,
  ADD_OVERRIDE_REGION: `${Namespace.REGIONLIST}.addOverrideRegion`,
  REMOVE_OVERRIDE_REGION: `${Namespace.REGIONLIST}.removeOverrideRegion`,
  PROXY_ENABLE: `${Namespace.PROXY}.enable`,
  PROXY_DISABLE: `${Namespace.PROXY}.disable`,
  PAC_UPDATE: `${Target.PAC}/update`,
  DOWNLOAD_BYPASS_JSON: `${Namespace.BYPASSLIST}.saveRulesToFile`,
  IMPORT_RULES: `${Namespace.BYPASSLIST}.importRules`,
  I18N_TRANSLATE: `${Namespace.I18N}.t`
};

async function sendMessage(target, type, data) {
  if (!Object.values(Target).includes(target)) {
    throw new Error(`invalid target: ${target}`);
  }

  if (!type) {
    throw new Error('invalid type');
  }

  const msg = {
    type,
    target,
    data: data || {}
  };
  return browser.runtime.sendMessage(msg);
}

function isTarget(message, target) {
  if (!message) {
    return false;
  }

  if (!message.target) {
    return false;
  }

  if (message.target !== target && message.target !== Target.ALL) {
    return false;
  }

  return true;
}

function isType(message, type) {
  if (!message) {
    return false;
  }

  if (!message.type) {
    return false;
  }

  if (!message.type === type) {
    return false;
  }

  return true;
}



/***/ }),
/* 5 */
/***/ (function(module, exports, __webpack_require__) {

// Thank's IE8 for his funny defineProperty
module.exports = !__webpack_require__(11)(function () {
  return Object.defineProperty({}, 'a', { get: function () { return 7; } }).a != 7;
});


/***/ }),
/* 6 */
/***/ (function(module, exports, __webpack_require__) {

var store = __webpack_require__(32)('wks');
var uid = __webpack_require__(31);
var Symbol = __webpack_require__(3).Symbol;
var USE_SYMBOL = typeof Symbol == 'function';

var $exports = module.exports = function (name) {
  return store[name] || (store[name] =
    USE_SYMBOL && Symbol[name] || (USE_SYMBOL ? Symbol : uid)('Symbol.' + name));
};

$exports.store = store;


/***/ }),
/* 7 */,
/* 8 */
/***/ (function(module, exports) {

module.exports = function (it) {
  return typeof it === 'object' ? it !== null : typeof it === 'function';
};


/***/ }),
/* 9 */
/***/ (function(module, exports, __webpack_require__) {

// 7.1.13 ToObject(argument)
var defined = __webpack_require__(39);
module.exports = function (it) {
  return Object(defined(it));
};


/***/ }),
/* 10 */
/***/ (function(module, exports, __webpack_require__) {

var anObject = __webpack_require__(17);
var IE8_DOM_DEFINE = __webpack_require__(50);
var toPrimitive = __webpack_require__(20);
var dP = Object.defineProperty;

exports.f = __webpack_require__(5) ? Object.defineProperty : function defineProperty(O, P, Attributes) {
  anObject(O);
  P = toPrimitive(P, true);
  anObject(Attributes);
  if (IE8_DOM_DEFINE) try {
    return dP(O, P, Attributes);
  } catch (e) { /* empty */ }
  if ('get' in Attributes || 'set' in Attributes) throw TypeError('Accessors not supported!');
  if ('value' in Attributes) O[P] = Attributes.value;
  return O;
};


/***/ }),
/* 11 */
/***/ (function(module, exports) {

module.exports = function (exec) {
  try {
    return !!exec();
  } catch (e) {
    return true;
  }
};


/***/ }),
/* 12 */
/***/ (function(module, exports) {

module.exports = function (it) {
  if (typeof it != 'function') throw TypeError(it + ' is not a function!');
  return it;
};


/***/ }),
/* 13 */
/***/ (function(module, exports, __webpack_require__) {

var dP = __webpack_require__(10);
var createDesc = __webpack_require__(29);
module.exports = __webpack_require__(5) ? function (object, key, value) {
  return dP.f(object, key, createDesc(1, value));
} : function (object, key, value) {
  object[key] = value;
  return object;
};


/***/ }),
/* 14 */
/***/ (function(module, exports, __webpack_require__) {

// to indexed object, toObject with fallback for non-array-like ES3 strings
var IObject = __webpack_require__(59);
var defined = __webpack_require__(39);
module.exports = function (it) {
  return IObject(defined(it));
};


/***/ }),
/* 15 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
const TIMED_OUT = Symbol('timed out');
/**
 * Schedule a promise to reject after "time" ms
 *
 * @param {number} time timeout before rejecting promise
 */

function wait(time) {
  return new Promise((_, reject) => {
    setTimeout(() => {
      reject(TIMED_OUT);
    }, time);
  });
}
/**
 * Add a timeout to a promise
 *
 * The resulting promise will reject if the timeout expires before
 * the given promise resolves/rejects
 *
 * @template T
 *
 * @param {Promise<T>} promise Given promise
 * @param {number} timeout Amount of time
 *
 * @returns {Promise<T>} wrapped promise
 */


function addTimeout(promise, timeout) {
  return Promise.race([promise, wait(timeout)]);
}
/**
 * Get a result from a request, be it with or without a timeout
 *
 * @param {Promise<Response>} request The pending result of fetch request
 * @param {number} [timeout] Possible timeout on request
 *
 * @throws {Response} if response is not ok
 * @throws {Symbol} if timeout expires
 * @throws {Error} if generic error occurs
 */


async function getResult(request, timeout) {
  let result;

  if (timeout > 0) {
    result = await addTimeout(request, timeout);
  } else {
    result = await request;
  }

  if (!result.ok) {
    throw result;
  }

  return result;
}
/**
 * Augment the provided error with cause and ok
 *
 * NOTE: Will fail to augment cyclic errors
 */


function augmentError(error, cause) {
  try {
    return Object.assign(error, {
      cause
    });
  } catch (_) {
    return Object.assign(JSON.parse(JSON.stringify(error, Object.getOwnPropertyNames(error))), {
      cause
    });
  }
}
/**
 * Add a cause to failed requests
 *
 * @param {Error|Response|Symbol} err thrown error from fetch request
 */


function addCause(err) {
  let errWithCause;

  if (err === TIMED_OUT) {
    errWithCause = augmentError(new Error('timeout occurred'), 'timeout');
  } else if (err.ok === false) {
    errWithCause = augmentError(err, 'status');
  } else if (!window.navigator.onLine) {
    errWithCause = augmentError(err, 'offline');
  } else {
    errWithCause = augmentError(err, 'error');
  }

  return errWithCause;
}
/**
 * Get opts for fetch, allowing each method to have
 * unique defaults, and assigning logical defaults
 * if no other value is provided
 *
 * Logical defaults are currently based on Chrome's
 * default values
 *
 * @param {*} methodOpts Opts defined for method
 * @param {*} clientOpts Opts defined by user
 */


function getOpts(methodOpts, clientOpts) {
  const {
    method
  } = methodOpts;

  if (!method) {
    throw new Error('methodOpts must contain method');
  }

  const mode = clientOpts.mode || methodOpts.mode;
  const credentials = clientOpts.credentials || methodOpts.credentials;
  const cache = clientOpts.cache || methodOpts.cache || 'default';
  const redirect = clientOpts.redirect || methodOpts.redirect || 'follow';
  const referrer = clientOpts.referrer || methodOpts.referrer || 'client';
  const integrity = clientOpts.integrity || methodOpts.integrity;
  const defaultHeaders = methodOpts.headers || {};
  const clientHeaders = clientOpts.headers || {};
  const headers = Object.assign({}, defaultHeaders, clientHeaders);
  const {
    body
  } = clientOpts;
  return {
    mode,
    body,
    credentials,
    cache,
    redirect,
    referrer,
    integrity,
    headers,
    method
  };
}
/**
 * Create a http request method utilizing native fetch api
 *
 * @param {*} methodOpts Optionally set logical defaults for the method
 */


function createMethod(methodOpts = {}) {
  return async (url, clientOpts = {}) => {
    if (!url) {
      throw new Error('must provide url for http requests');
    } // extract timeout (not native fetch opt)


    const {
      timeout
    } = clientOpts;
    const opts = getOpts(methodOpts, clientOpts);
    const request = fetch(url, opts);

    try {
      // Await is important here in order to catch rejected promise
      return await getResult(request, timeout);
    } catch (err) {
      throw addCause(err);
    }
  };
}
/**
 * Utility for making http requests
 */


const http = {
  get: createMethod({
    method: 'GET'
  }),
  head: createMethod({
    method: 'HEAD'
  }),
  post: createMethod({
    method: 'POST'
  })
};
/* harmony default export */ __webpack_exports__["a"] = (http);

/***/ }),
/* 16 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/*
   This object wraps a ChromeSetting: https://developer.chrome.com/extensions/types#type-ChromeSetting
   Similar to but not the same as a ContentSetting.
*/
class ChromeSetting {
  static get controllable() {
    return 'controllable_by_this_extension';
  }

  static get controlled() {
    return 'controlled_by_this_extension';
  }

  static get notControllable() {
    return 'not_controllable';
  }

  static get defaultSetOptions() {
    return {
      scope: 'regular'
    };
  }

  static get defaultGetOptions() {
    return {};
  }

  static get defaultClearOptions() {
    return {
      scope: 'regular'
    };
  }

  constructor(setting) {
    // init
    this.setting = setting;
  }

  async init() {
    if (this.isAvailable()) {
      // This API is currently missing on Firefox but documented as existing:
      // https://developer.mozilla.org/en-US/Add-ons/WebExtensions/API/types/BrowserSetting/onChange
      if (this.setting.onChange) {
        this.setting.onChange.addListener(this.onChange);
      }

      await this.get();
    } else {
      this.setLevelOfControl(ChromeSetting.notControllable);
      this.setBlocked(true);
    }
  }

  isAvailable() {
    return !!this.setting;
  } // eslint-disable-next-line class-methods-use-this


  onChange() {
    throw new Error('Each chromesetting must implement onChange');
  }

  getLevelOfControl() {
    return this.levelOfControl;
  }

  setLevelOfControl(levelOfControl) {
    this.levelOfControl = levelOfControl;
  }

  isControllable() {
    return this.levelOfControl === ChromeSetting.controllable || this.levelOfControl === ChromeSetting.controlled;
  }

  isBlocked() {
    return this.blocked;
  }

  setBlocked(blocked) {
    this.blocked = blocked;
  }

  isApplied() {
    return this.applied;
  }

  set(options, override) {
    return new Promise((resolve, reject) => {
      if (this.isControllable()) {
        this.setting.set(Object.assign({}, ChromeSetting.defaultSetOptions, options), () => {
          if (chrome.runtime.lastError === null) {
            if (override && override.applyValue) {
              this.applied = options.value;
            } else {
              this.applied = true;
            }

            resolve();
          } else {
            reject(chrome.runtime.lastError);
          }
        });
      } else {
        reject(new Error(`${this.settingID}: extension cannot control this setting`));
      }
    });
  }

  get() {
    return new Promise((resolve, reject) => {
      if (this.isAvailable()) {
        this.setting.get(ChromeSetting.defaultGetOptions, async details => {
          await Promise.resolve(this.onChange(details));

          if (chrome.runtime.lastError === null) {
            resolve(details);
          } else {
            reject(chrome.runtime.lastError);
          }
        });
      } else {
        reject(new Error(`${this.settingID} setting is not available`));
      }
    });
  }

  clear(options) {
    return new Promise((resolve, reject) => {
      if (this.isControllable()) {
        this.setting.clear(Object.assign({}, ChromeSetting.defaultClearOptions, options), () => {
          if (chrome.runtime.lastError === null) {
            this.applied = false;
            resolve();
          } else {
            reject(chrome.runtime.lastError);
          }
        });
      } else {
        reject(new Error(`${this.settingID}: extension cannot control this setting`));
      }
    });
  }

  createApplySetting(value, name, action) {
    return async function applySetting() {
      try {
        await this.set({
          value
        });
        ChromeSetting.debug(name, `${action} ok`);
      } catch (err) {
        ChromeSetting.debug(name, `${action} failed`);
      }

      return this;
    }.bind(this);
  }

  createClearSetting(name, action) {
    return async function clearSetting() {
      try {
        await this.clear();
        ChromeSetting.debug(name, `${action} ok`);
      } catch (err) {
        ChromeSetting.debug(name, `${action} failed`);
      }

      return this;
    }.bind(this);
  }

  static debug(name, msg, err) {
    const debugMsg = `${name}.js: ${msg}`;
    debug(debugMsg);

    if (err) {
      const errMsg = `error: ${JSON.stringify(err, Object.getOwnPropertyNames(err))}`;
      debug(errMsg);
    }

    return new Error(debugMsg);
  }

}

/* harmony default export */ __webpack_exports__["a"] = (ChromeSetting);

/***/ }),
/* 17 */
/***/ (function(module, exports, __webpack_require__) {

var isObject = __webpack_require__(8);
module.exports = function (it) {
  if (!isObject(it)) throw TypeError(it + ' is not an object!');
  return it;
};


/***/ }),
/* 18 */
/***/ (function(module, exports) {

var core = module.exports = { version: '2.6.12' };
if (typeof __e == 'number') __e = core; // eslint-disable-line no-undef


/***/ }),
/* 19 */
/***/ (function(module, exports) {

var hasOwnProperty = {}.hasOwnProperty;
module.exports = function (it, key) {
  return hasOwnProperty.call(it, key);
};


/***/ }),
/* 20 */
/***/ (function(module, exports, __webpack_require__) {

// 7.1.1 ToPrimitive(input [, PreferredType])
var isObject = __webpack_require__(8);
// instead of the ES6 spec version, we didn't implement @@toPrimitive case
// and the second argument - flag - preferred type is a string
module.exports = function (it, S) {
  if (!isObject(it)) return it;
  var fn, val;
  if (S && typeof (fn = it.toString) == 'function' && !isObject(val = fn.call(it))) return val;
  if (typeof (fn = it.valueOf) == 'function' && !isObject(val = fn.call(it))) return val;
  if (!S && typeof (fn = it.toString) == 'function' && !isObject(val = fn.call(it))) return val;
  throw TypeError("Can't convert object to primitive value");
};


/***/ }),
/* 21 */
/***/ (function(module, exports) {

module.exports = false;


/***/ }),
/* 22 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return createApplyListener; });
function createApplyListener(fn) {
  return (app, api) => {
    fn(app, api.addListener.bind(api));
  };
}

/***/ }),
/* 23 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/*
   This object wraps a ChromeSetting: https://developer.chrome.com/extensions/types#type-ChromeSetting
   Similar to but not the same as a ContentSetting.
*/
class ChromeSetting {
  static get defaultSetOptions() {
    return {
      scope: 'regular'
    };
  }

  static get defaultGetOptions() {
    return {};
  }

  static get defaultClearOptions() {
    return {
      scope: 'regular'
    };
  }

  static get controlled() {
    return 'controlled_by_this_extension';
  }

  static get controllable() {
    return 'controllable_by_this_extension';
  }

  static get notControllable() {
    return 'not_controllable';
  }

  constructor(setting) {
    // bindings
    this.init = this.init.bind(this);
    this.getLevelOfControl = this.getLevelOfControl.bind(this);
    this.isControllable = this.isControllable.bind(this);
    this.isBlocked = this.isBlocked.bind(this);
    this.isApplied = this.isApplied.bind(this);
    this.onChange = this.onChange.bind(this);
    this.set = this.set.bind(this);
    this.get = this.get.bind(this);
    this.clear = this.clear.bind(this);
    this.createApplySetting = this.createApplySetting.bind(this);
    this.createClearSetting = this.createClearSetting.bind(this); // init

    this.setting = setting;
    this.levelOfControl = undefined;
    this.blocked = undefined;
    this.applied = undefined;
  }

  async init() {
    if (this.isAvailable()) {
      this.setting.onChange.addListener(this.onChange);
      await this.setting.get({}, this.onChange);
    } else {
      this.setLevelOfControl(ChromeSetting.notControllable);
      this.blocked = true;
    }
  }

  isAvailable() {
    return !!this.setting;
  } // eslint-disable-next-line class-methods-use-this


  onChange() {
    throw new Error('each chromesetting must implement it\'s own onChange listener');
  }
  /**
   * Get the current level of control
   *
   * @returns {string} current level of control
   */


  getLevelOfControl() {
    return this.levelOfControl;
  }

  setLevelOfControl(levelOfControl) {
    this.levelOfControl = levelOfControl;
  }
  /**
   * Determine whether the setting is controllable
   *
   * @returns {boolean} whether setting is controllable
   */


  isControllable() {
    return this.levelOfControl === undefined || this.levelOfControl === ChromeSetting.controlled || this.levelOfControl === ChromeSetting.controllable;
  }
  /**
   * Determine whether or not the setting is blocked
   *
   * @returns {boolean} whether setting is blocked
   */


  isBlocked() {
    return this.blocked;
  }

  setBlocked(blocked) {
    this.blocked = blocked;
  }
  /**
   * Determine whether or not setting is applied
   *
   * @returns {boolean} whether setting is applied
   */


  isApplied() {
    return this.applied;
  }
  /**
   * Set the info for the setting
   */


  set(options) {
    return new Promise((resolve, reject) => {
      if (this.isControllable()) {
        this.setting.set(Object.assign({}, ChromeSetting.defaultSetOptions, options), () => {
          if (chrome.runtime.lastError === undefined) {
            this.applied = true;
            resolve();
          } else {
            reject(chrome.runtime.lastError);
          }
        });
      } else {
        reject(new Error('extension cannot control this setting'));
      }
    });
  }
  /**
   * Get the current info for setting
   */


  get() {
    return new Promise((resolve, reject) => {
      if (!this.isAvailable()) {
        reject();
        return;
      }

      this.setting.get(ChromeSetting.defaultGetOptions, async details => {
        await this.onChange(details);

        if (chrome.runtime.lastError === undefined) {
          resolve(details);
        } else {
          reject(chrome.runtime.lastError);
        }
      });
    });
  }
  /**
   * Clear the info for the setting
   */


  clear(options) {
    return new Promise((resolve, reject) => {
      if (this.isControllable()) {
        this.setting.clear(Object.assign({}, ChromeSetting.defaultClearOptions, options || {}), () => {
          if (chrome.runtime.lastError === undefined) {
            this.applied = false;
            resolve();
          } else {
            reject(chrome.runtime.lastError);
          }
        });
      } else {
        reject(new Error('extension cannot control this setting'));
      }
    });
  }

  createApplySetting(value, name, action) {
    return async function applySetting() {
      try {
        await this.set({
          value
        });
        ChromeSetting.debug(name, `${action} ok`);
      } catch (err) {
        ChromeSetting.debug(name, `${action} failed`);
      }

      return this;
    }.bind(this);
  }

  createClearSetting(name, action) {
    return async function clearSetting() {
      try {
        await this.clear();
        ChromeSetting.debug(name, `${action} ok`);
      } catch (err) {
        ChromeSetting.debug(name, `${action} failed`);
      }

      return this;
    }.bind(this);
  }

  static debug(name, msg, err) {
    const debugMsg = `${name}.js: ${msg}`;
    debug(debugMsg);

    if (err) {
      const errMsg = `error: ${JSON.stringify(err, Object.getOwnPropertyNames(err))}`;
      debug(errMsg);
    }

    return new Error(debugMsg);
  }

}

/* harmony default export */ __webpack_exports__["a"] = (ChromeSetting);

/***/ }),
/* 24 */,
/* 25 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "f", function() { return MessageType; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "e", function() { return LATEST_TIMESTAMP_FILE; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "h", function() { return RULESET_FILE_TEMPLATE; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "d", function() { return LAST_UPDATED_KEY; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "c", function() { return LAST_TIMESTAMP_KEY; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "j", function() { return STORAGE_TEMPLATE; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "i", function() { return STORAGE_COUNT_KEY; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "k", function() { return channels; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "b", function() { return COUNTER_LIMIT; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "g", function() { return PART_SIZE; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return ALARM_NAME; });
// ======================================== //
//                Messaging                 //
// ======================================== //
const MessageType = {
  EXTRACT_REQ: 'extract',
  EXTRACT_RES: 'extract_response'
}; // ======================================== //
//                  Files                   //
// ======================================== //

const LATEST_TIMESTAMP_FILE = 'eff.default.ruleset.timestamp';
const RULESET_FILE_TEMPLATE = 'eff.default.ruleset.latest.gz'; // ======================================== //
//               Storage Keys               //
// ======================================== //

const STORAGE_PREFIX = 'https-upgrade';
const LAST_UPDATED_KEY = `${STORAGE_PREFIX}::last-updated`;
const LAST_TIMESTAMP_KEY = `${STORAGE_PREFIX}::last-timestamp`;
const STORAGE_TEMPLATE = `${STORAGE_PREFIX}::%s`;
const STORAGE_COUNT_KEY = `${STORAGE_PREFIX}::storage-count`; // ======================================== //
//                 Channels                 //
// ======================================== //

const channels = [{
  name: 'default',
  urlPrefix: 'https://s3.amazonaws.com/privateinternetaccess/'
}]; // ======================================== //
//                  General                 //
// ======================================== //

const COUNTER_LIMIT = 6;
const PART_SIZE = 500;
const ALARM_NAME = 'PollHttpsRules';

/***/ }),
/* 26 */
/***/ (function(module, exports, __webpack_require__) {

// 19.1.2.14 / 15.2.3.14 Object.keys(O)
var $keys = __webpack_require__(61);
var enumBugKeys = __webpack_require__(44);

module.exports = Object.keys || function keys(O) {
  return $keys(O, enumBugKeys);
};


/***/ }),
/* 27 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

// Forced replacement prototype accessors methods
module.exports = __webpack_require__(21) || !__webpack_require__(11)(function () {
  var K = Math.random();
  // In FF throws only define methods
  // eslint-disable-next-line no-undef, no-useless-call
  __defineSetter__.call(null, K, function () { /* empty */ });
  delete __webpack_require__(3)[K];
});


/***/ }),
/* 28 */
/***/ (function(module, exports, __webpack_require__) {

var pIE = __webpack_require__(42);
var createDesc = __webpack_require__(29);
var toIObject = __webpack_require__(14);
var toPrimitive = __webpack_require__(20);
var has = __webpack_require__(19);
var IE8_DOM_DEFINE = __webpack_require__(50);
var gOPD = Object.getOwnPropertyDescriptor;

exports.f = __webpack_require__(5) ? gOPD : function getOwnPropertyDescriptor(O, P) {
  O = toIObject(O);
  P = toPrimitive(P, true);
  if (IE8_DOM_DEFINE) try {
    return gOPD(O, P);
  } catch (e) { /* empty */ }
  if (has(O, P)) return createDesc(!pIE.f.call(O, P), O[P]);
};


/***/ }),
/* 29 */
/***/ (function(module, exports) {

module.exports = function (bitmap, value) {
  return {
    enumerable: !(bitmap & 1),
    configurable: !(bitmap & 2),
    writable: !(bitmap & 4),
    value: value
  };
};


/***/ }),
/* 30 */
/***/ (function(module, exports, __webpack_require__) {

var global = __webpack_require__(3);
var hide = __webpack_require__(13);
var has = __webpack_require__(19);
var SRC = __webpack_require__(31)('src');
var $toString = __webpack_require__(77);
var TO_STRING = 'toString';
var TPL = ('' + $toString).split(TO_STRING);

__webpack_require__(18).inspectSource = function (it) {
  return $toString.call(it);
};

(module.exports = function (O, key, val, safe) {
  var isFunction = typeof val == 'function';
  if (isFunction) has(val, 'name') || hide(val, 'name', key);
  if (O[key] === val) return;
  if (isFunction) has(val, SRC) || hide(val, SRC, O[key] ? '' + O[key] : TPL.join(String(key)));
  if (O === global) {
    O[key] = val;
  } else if (!safe) {
    delete O[key];
    hide(O, key, val);
  } else if (O[key]) {
    O[key] = val;
  } else {
    hide(O, key, val);
  }
// add fake Function#toString for correct work wrapped methods / constructors with methods like LoDash isNative
})(Function.prototype, TO_STRING, function toString() {
  return typeof this == 'function' && this[SRC] || $toString.call(this);
});


/***/ }),
/* 31 */
/***/ (function(module, exports) {

var id = 0;
var px = Math.random();
module.exports = function (key) {
  return 'Symbol('.concat(key === undefined ? '' : key, ')_', (++id + px).toString(36));
};


/***/ }),
/* 32 */
/***/ (function(module, exports, __webpack_require__) {

var core = __webpack_require__(18);
var global = __webpack_require__(3);
var SHARED = '__core-js_shared__';
var store = global[SHARED] || (global[SHARED] = {});

(module.exports = function (key, value) {
  return store[key] || (store[key] = value !== undefined ? value : {});
})('versions', []).push({
  version: core.version,
  mode: __webpack_require__(21) ? 'pure' : 'global',
  copyright: '© 2020 Denis Pushkarev (zloirock.ru)'
});


/***/ }),
/* 33 */
/***/ (function(module, exports, __webpack_require__) {

// optional / simple context binding
var aFunction = __webpack_require__(12);
module.exports = function (fn, that, length) {
  aFunction(fn);
  if (that === undefined) return fn;
  switch (length) {
    case 1: return function (a) {
      return fn.call(that, a);
    };
    case 2: return function (a, b) {
      return fn.call(that, a, b);
    };
    case 3: return function (a, b, c) {
      return fn.call(that, a, b, c);
    };
  }
  return function (/* ...args */) {
    return fn.apply(that, arguments);
  };
};


/***/ }),
/* 34 */
/***/ (function(module, exports) {

var toString = {}.toString;

module.exports = function (it) {
  return toString.call(it).slice(8, -1);
};


/***/ }),
/* 35 */
/***/ (function(module, exports, __webpack_require__) {

// 19.1.2.9 / 15.2.3.2 Object.getPrototypeOf(O)
var has = __webpack_require__(19);
var toObject = __webpack_require__(9);
var IE_PROTO = __webpack_require__(41)('IE_PROTO');
var ObjectProto = Object.prototype;

module.exports = Object.getPrototypeOf || function (O) {
  O = toObject(O);
  if (has(O, IE_PROTO)) return O[IE_PROTO];
  if (typeof O.constructor == 'function' && O instanceof O.constructor) {
    return O.constructor.prototype;
  } return O instanceof Object ? ObjectProto : null;
};


/***/ }),
/* 36 */
/***/ (function(module, exports, __webpack_require__) {

// most Object methods by ES6 should accept primitives
var $export = __webpack_require__(2);
var core = __webpack_require__(18);
var fails = __webpack_require__(11);
module.exports = function (KEY, exec) {
  var fn = (core.Object || {})[KEY] || Object[KEY];
  var exp = {};
  exp[KEY] = exec(fn);
  $export($export.S + $export.F * fails(function () { fn(1); }), 'Object', exp);
};


/***/ }),
/* 37 */
/***/ (function(module, exports, __webpack_require__) {

var isObject = __webpack_require__(8);
var document = __webpack_require__(3).document;
// typeof document.createElement is 'object' in old IE
var is = isObject(document) && isObject(document.createElement);
module.exports = function (it) {
  return is ? document.createElement(it) : {};
};


/***/ }),
/* 38 */
/***/ (function(module, exports, __webpack_require__) {

// 7.1.15 ToLength
var toInteger = __webpack_require__(51);
var min = Math.min;
module.exports = function (it) {
  return it > 0 ? min(toInteger(it), 0x1fffffffffffff) : 0; // pow(2, 53) - 1 == 9007199254740991
};


/***/ }),
/* 39 */
/***/ (function(module, exports) {

// 7.2.1 RequireObjectCoercible(argument)
module.exports = function (it) {
  if (it == undefined) throw TypeError("Can't call method on  " + it);
  return it;
};


/***/ }),
/* 40 */
/***/ (function(module, exports) {

module.exports = {};


/***/ }),
/* 41 */
/***/ (function(module, exports, __webpack_require__) {

var shared = __webpack_require__(32)('keys');
var uid = __webpack_require__(31);
module.exports = function (key) {
  return shared[key] || (shared[key] = uid(key));
};


/***/ }),
/* 42 */
/***/ (function(module, exports) {

exports.f = {}.propertyIsEnumerable;


/***/ }),
/* 43 */
/***/ (function(module, exports, __webpack_require__) {

// 7.2.2 IsArray(argument)
var cof = __webpack_require__(34);
module.exports = Array.isArray || function isArray(arg) {
  return cof(arg) == 'Array';
};


/***/ }),
/* 44 */
/***/ (function(module, exports) {

// IE 8- don't enum bug keys
module.exports = (
  'constructor,hasOwnProperty,isPrototypeOf,propertyIsEnumerable,toLocaleString,toString,valueOf'
).split(',');


/***/ }),
/* 45 */
/***/ (function(module, exports, __webpack_require__) {

var def = __webpack_require__(10).f;
var has = __webpack_require__(19);
var TAG = __webpack_require__(6)('toStringTag');

module.exports = function (it, tag, stat) {
  if (it && !has(it = stat ? it : it.prototype, TAG)) def(it, TAG, { configurable: true, value: tag });
};


/***/ }),
/* 46 */,
/* 47 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var addToUnscopables = __webpack_require__(52);
var step = __webpack_require__(81);
var Iterators = __webpack_require__(40);
var toIObject = __webpack_require__(14);

// 22.1.3.4 Array.prototype.entries()
// 22.1.3.13 Array.prototype.keys()
// 22.1.3.29 Array.prototype.values()
// 22.1.3.30 Array.prototype[@@iterator]()
module.exports = __webpack_require__(82)(Array, 'Array', function (iterated, kind) {
  this._t = toIObject(iterated); // target
  this._i = 0;                   // next index
  this._k = kind;                // kind
// 22.1.5.2.1 %ArrayIteratorPrototype%.next()
}, function () {
  var O = this._t;
  var kind = this._k;
  var index = this._i++;
  if (!O || index >= O.length) {
    this._t = undefined;
    return step(1);
  }
  if (kind == 'keys') return step(0, index);
  if (kind == 'values') return step(0, O[index]);
  return step(0, [index, O[index]]);
}, 'values');

// argumentsList[@@iterator] is %ArrayProto_values% (9.4.4.6, 9.4.4.7)
Iterators.Arguments = Iterators.Array;

addToUnscopables('keys');
addToUnscopables('values');
addToUnscopables('entries');


/***/ }),
/* 48 */
/***/ (function(module, exports, __webpack_require__) {

// 19.1.2.2 / 15.2.3.5 Object.create(O [, Properties])
var anObject = __webpack_require__(17);
var dPs = __webpack_require__(60);
var enumBugKeys = __webpack_require__(44);
var IE_PROTO = __webpack_require__(41)('IE_PROTO');
var Empty = function () { /* empty */ };
var PROTOTYPE = 'prototype';

// Create object with fake `null` prototype: use iframe Object with cleared prototype
var createDict = function () {
  // Thrash, waste and sodomy: IE GC bug
  var iframe = __webpack_require__(37)('iframe');
  var i = enumBugKeys.length;
  var lt = '<';
  var gt = '>';
  var iframeDocument;
  iframe.style.display = 'none';
  __webpack_require__(53).appendChild(iframe);
  iframe.src = 'javascript:'; // eslint-disable-line no-script-url
  // createDict = iframe.contentWindow.Object;
  // html.removeChild(iframe);
  iframeDocument = iframe.contentWindow.document;
  iframeDocument.open();
  iframeDocument.write(lt + 'script' + gt + 'document.F=Object' + lt + '/script' + gt);
  iframeDocument.close();
  createDict = iframeDocument.F;
  while (i--) delete createDict[PROTOTYPE][enumBugKeys[i]];
  return createDict();
};

module.exports = Object.create || function create(O, Properties) {
  var result;
  if (O !== null) {
    Empty[PROTOTYPE] = anObject(O);
    result = new Empty();
    Empty[PROTOTYPE] = null;
    // add "__proto__" for Object.getPrototypeOf polyfill
    result[IE_PROTO] = O;
  } else result = createDict();
  return Properties === undefined ? result : dPs(result, Properties);
};


/***/ }),
/* 49 */,
/* 50 */
/***/ (function(module, exports, __webpack_require__) {

module.exports = !__webpack_require__(5) && !__webpack_require__(11)(function () {
  return Object.defineProperty(__webpack_require__(37)('div'), 'a', { get: function () { return 7; } }).a != 7;
});


/***/ }),
/* 51 */
/***/ (function(module, exports) {

// 7.1.4 ToInteger
var ceil = Math.ceil;
var floor = Math.floor;
module.exports = function (it) {
  return isNaN(it = +it) ? 0 : (it > 0 ? floor : ceil)(it);
};


/***/ }),
/* 52 */
/***/ (function(module, exports, __webpack_require__) {

// 22.1.3.31 Array.prototype[@@unscopables]
var UNSCOPABLES = __webpack_require__(6)('unscopables');
var ArrayProto = Array.prototype;
if (ArrayProto[UNSCOPABLES] == undefined) __webpack_require__(13)(ArrayProto, UNSCOPABLES, {});
module.exports = function (key) {
  ArrayProto[UNSCOPABLES][key] = true;
};


/***/ }),
/* 53 */
/***/ (function(module, exports, __webpack_require__) {

var document = __webpack_require__(3).document;
module.exports = document && document.documentElement;


/***/ }),
/* 54 */
/***/ (function(module, exports, __webpack_require__) {

var $export = __webpack_require__(2);
var defined = __webpack_require__(39);
var fails = __webpack_require__(11);
var spaces = __webpack_require__(90);
var space = '[' + spaces + ']';
var non = '\u200b\u0085';
var ltrim = RegExp('^' + space + space + '*');
var rtrim = RegExp(space + space + '*$');

var exporter = function (KEY, exec, ALIAS) {
  var exp = {};
  var FORCE = fails(function () {
    return !!spaces[KEY]() || non[KEY]() != non;
  });
  var fn = exp[KEY] = FORCE ? exec(trim) : spaces[KEY];
  if (ALIAS) exp[ALIAS] = fn;
  $export($export.P + $export.F * FORCE, 'String', exp);
};

// 1 -> String#trimLeft
// 2 -> String#trimRight
// 3 -> String#trim
var trim = exporter.trim = function (string, TYPE) {
  string = String(defined(string));
  if (TYPE & 1) string = string.replace(ltrim, '');
  if (TYPE & 2) string = string.replace(rtrim, '');
  return string;
};

module.exports = exporter;


/***/ }),
/* 55 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var $export = __webpack_require__(2);
var toObject = __webpack_require__(9);
var aFunction = __webpack_require__(12);
var $defineProperty = __webpack_require__(10);

// B.2.2.2 Object.prototype.__defineGetter__(P, getter)
__webpack_require__(5) && $export($export.P + __webpack_require__(27), 'Object', {
  __defineGetter__: function __defineGetter__(P, getter) {
    $defineProperty.f(toObject(this), P, { get: aFunction(getter), enumerable: true, configurable: true });
  }
});


/***/ }),
/* 56 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var $export = __webpack_require__(2);
var toObject = __webpack_require__(9);
var aFunction = __webpack_require__(12);
var $defineProperty = __webpack_require__(10);

// B.2.2.3 Object.prototype.__defineSetter__(P, setter)
__webpack_require__(5) && $export($export.P + __webpack_require__(27), 'Object', {
  __defineSetter__: function __defineSetter__(P, setter) {
    $defineProperty.f(toObject(this), P, { set: aFunction(setter), enumerable: true, configurable: true });
  }
});


/***/ }),
/* 57 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var $export = __webpack_require__(2);
var toObject = __webpack_require__(9);
var toPrimitive = __webpack_require__(20);
var getPrototypeOf = __webpack_require__(35);
var getOwnPropertyDescriptor = __webpack_require__(28).f;

// B.2.2.4 Object.prototype.__lookupGetter__(P)
__webpack_require__(5) && $export($export.P + __webpack_require__(27), 'Object', {
  __lookupGetter__: function __lookupGetter__(P) {
    var O = toObject(this);
    var K = toPrimitive(P, true);
    var D;
    do {
      if (D = getOwnPropertyDescriptor(O, K)) return D.get;
    } while (O = getPrototypeOf(O));
  }
});


/***/ }),
/* 58 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var $export = __webpack_require__(2);
var toObject = __webpack_require__(9);
var toPrimitive = __webpack_require__(20);
var getPrototypeOf = __webpack_require__(35);
var getOwnPropertyDescriptor = __webpack_require__(28).f;

// B.2.2.5 Object.prototype.__lookupSetter__(P)
__webpack_require__(5) && $export($export.P + __webpack_require__(27), 'Object', {
  __lookupSetter__: function __lookupSetter__(P) {
    var O = toObject(this);
    var K = toPrimitive(P, true);
    var D;
    do {
      if (D = getOwnPropertyDescriptor(O, K)) return D.set;
    } while (O = getPrototypeOf(O));
  }
});


/***/ }),
/* 59 */
/***/ (function(module, exports, __webpack_require__) {

// fallback for non-array-like ES3 and non-enumerable old V8 strings
var cof = __webpack_require__(34);
// eslint-disable-next-line no-prototype-builtins
module.exports = Object('z').propertyIsEnumerable(0) ? Object : function (it) {
  return cof(it) == 'String' ? it.split('') : Object(it);
};


/***/ }),
/* 60 */
/***/ (function(module, exports, __webpack_require__) {

var dP = __webpack_require__(10);
var anObject = __webpack_require__(17);
var getKeys = __webpack_require__(26);

module.exports = __webpack_require__(5) ? Object.defineProperties : function defineProperties(O, Properties) {
  anObject(O);
  var keys = getKeys(Properties);
  var length = keys.length;
  var i = 0;
  var P;
  while (length > i) dP.f(O, P = keys[i++], Properties[P]);
  return O;
};


/***/ }),
/* 61 */
/***/ (function(module, exports, __webpack_require__) {

var has = __webpack_require__(19);
var toIObject = __webpack_require__(14);
var arrayIndexOf = __webpack_require__(84)(false);
var IE_PROTO = __webpack_require__(41)('IE_PROTO');

module.exports = function (object, names) {
  var O = toIObject(object);
  var i = 0;
  var result = [];
  var key;
  for (key in O) if (key != IE_PROTO) has(O, key) && result.push(key);
  // Don't enum bug & hidden keys
  while (names.length > i) if (has(O, key = names[i++])) {
    ~arrayIndexOf(result, key) || result.push(key);
  }
  return result;
};


/***/ }),
/* 62 */
/***/ (function(module, exports, __webpack_require__) {

var global = __webpack_require__(3);
var core = __webpack_require__(18);
var LIBRARY = __webpack_require__(21);
var wksExt = __webpack_require__(63);
var defineProperty = __webpack_require__(10).f;
module.exports = function (name) {
  var $Symbol = core.Symbol || (core.Symbol = LIBRARY ? {} : global.Symbol || {});
  if (name.charAt(0) != '_' && !(name in $Symbol)) defineProperty($Symbol, name, { value: wksExt.f(name) });
};


/***/ }),
/* 63 */
/***/ (function(module, exports, __webpack_require__) {

exports.f = __webpack_require__(6);


/***/ }),
/* 64 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/**
 * report an error if debug mode enabled
 *
 * @param {string} name context for error
 * @param {Error} err error
 */
function reportError(...args) {
  const [name] = args;

  const act = err => {
    let errorMessage;

    if (typeof err === 'string') {
      errorMessage = err;
    } else {
      errorMessage = JSON.stringify(err, Object.getOwnPropertyNames(err));
    }

    debug(`${name}: ${errorMessage}`);
  };

  if (args.length > 1) {
    const err = args[1];
    return act(err);
  }

  return act;
}

/* harmony default export */ __webpack_exports__["a"] = (reportError);

/***/ }),
/* 65 */,
/* 66 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

// https://tc39.github.io/proposal-flatMap/#sec-Array.prototype.flatMap
var $export = __webpack_require__(2);
var flattenIntoArray = __webpack_require__(78);
var toObject = __webpack_require__(9);
var toLength = __webpack_require__(38);
var aFunction = __webpack_require__(12);
var arraySpeciesCreate = __webpack_require__(79);

$export($export.P, 'Array', {
  flatMap: function flatMap(callbackfn /* , thisArg */) {
    var O = toObject(this);
    var sourceLen, A;
    aFunction(callbackfn);
    sourceLen = toLength(O.length);
    A = arraySpeciesCreate(O, 0);
    flattenIntoArray(A, O, O, sourceLen, 0, 1, callbackfn, arguments[1]);
    return A;
  }
});

__webpack_require__(52)('flatMap');


/***/ }),
/* 67 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var $export = __webpack_require__(2);
var aFunction = __webpack_require__(12);
var toObject = __webpack_require__(9);
var fails = __webpack_require__(11);
var $sort = [].sort;
var test = [1, 2, 3];

$export($export.P + $export.F * (fails(function () {
  // IE8-
  test.sort(undefined);
}) || !fails(function () {
  // V8 bug
  test.sort(null);
  // Old WebKit
}) || !__webpack_require__(86)($sort)), 'Array', {
  // 22.1.3.25 Array.prototype.sort(comparefn)
  sort: function sort(comparefn) {
    return comparefn === undefined
      ? $sort.call(toObject(this))
      : $sort.call(toObject(this), aFunction(comparefn));
  }
});


/***/ }),
/* 68 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";
// https://github.com/tc39/proposal-promise-finally

var $export = __webpack_require__(2);
var core = __webpack_require__(18);
var global = __webpack_require__(3);
var speciesConstructor = __webpack_require__(87);
var promiseResolve = __webpack_require__(88);

$export($export.P + $export.R, 'Promise', { 'finally': function (onFinally) {
  var C = speciesConstructor(this, core.Promise || global.Promise);
  var isFunction = typeof onFinally == 'function';
  return this.then(
    isFunction ? function (x) {
      return promiseResolve(C, onFinally()).then(function () { return x; });
    } : onFinally,
    isFunction ? function (e) {
      return promiseResolve(C, onFinally()).then(function () { throw e; });
    } : onFinally
  );
} });


/***/ }),
/* 69 */
/***/ (function(module, exports, __webpack_require__) {

__webpack_require__(62)('asyncIterator');


/***/ }),
/* 70 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

// https://github.com/sebmarkbage/ecmascript-string-left-right-trim
__webpack_require__(54)('trimLeft', function ($trim) {
  return function trimLeft() {
    return $trim(this, 1);
  };
}, 'trimStart');


/***/ }),
/* 71 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

// https://github.com/sebmarkbage/ecmascript-string-left-right-trim
__webpack_require__(54)('trimRight', function ($trim) {
  return function trimRight() {
    return $trim(this, 2);
  };
}, 'trimEnd');


/***/ }),
/* 72 */
/***/ (function(module, exports, __webpack_require__) {

// ie9- setTimeout & setInterval additional parameters fix
var global = __webpack_require__(3);
var $export = __webpack_require__(2);
var userAgent = __webpack_require__(91);
var slice = [].slice;
var MSIE = /MSIE .\./.test(userAgent); // <- dirty ie9- check
var wrap = function (set) {
  return function (fn, time /* , ...args */) {
    var boundArgs = arguments.length > 2;
    var args = boundArgs ? slice.call(arguments, 2) : false;
    return set(boundArgs ? function () {
      // eslint-disable-next-line no-new-func
      (typeof fn == 'function' ? fn : Function(fn)).apply(this, args);
    } : fn, time);
  };
};
$export($export.G + $export.B + $export.F * MSIE, {
  setTimeout: wrap(global.setTimeout),
  setInterval: wrap(global.setInterval)
});


/***/ }),
/* 73 */
/***/ (function(module, exports, __webpack_require__) {

var $export = __webpack_require__(2);
var $task = __webpack_require__(92);
$export($export.G + $export.B, {
  setImmediate: $task.set,
  clearImmediate: $task.clear
});


/***/ }),
/* 74 */
/***/ (function(module, exports, __webpack_require__) {

var $iterators = __webpack_require__(47);
var getKeys = __webpack_require__(26);
var redefine = __webpack_require__(30);
var global = __webpack_require__(3);
var hide = __webpack_require__(13);
var Iterators = __webpack_require__(40);
var wks = __webpack_require__(6);
var ITERATOR = wks('iterator');
var TO_STRING_TAG = wks('toStringTag');
var ArrayValues = Iterators.Array;

var DOMIterables = {
  CSSRuleList: true, // TODO: Not spec compliant, should be false.
  CSSStyleDeclaration: false,
  CSSValueList: false,
  ClientRectList: false,
  DOMRectList: false,
  DOMStringList: false,
  DOMTokenList: true,
  DataTransferItemList: false,
  FileList: false,
  HTMLAllCollection: false,
  HTMLCollection: false,
  HTMLFormElement: false,
  HTMLSelectElement: false,
  MediaList: true, // TODO: Not spec compliant, should be false.
  MimeTypeArray: false,
  NamedNodeMap: false,
  NodeList: true,
  PaintRequestList: false,
  Plugin: false,
  PluginArray: false,
  SVGLengthList: false,
  SVGNumberList: false,
  SVGPathSegList: false,
  SVGPointList: false,
  SVGStringList: false,
  SVGTransformList: false,
  SourceBufferList: false,
  StyleSheetList: true, // TODO: Not spec compliant, should be false.
  TextTrackCueList: false,
  TextTrackList: false,
  TouchList: false
};

for (var collections = getKeys(DOMIterables), i = 0; i < collections.length; i++) {
  var NAME = collections[i];
  var explicit = DOMIterables[NAME];
  var Collection = global[NAME];
  var proto = Collection && Collection.prototype;
  var key;
  if (proto) {
    if (!proto[ITERATOR]) hide(proto, ITERATOR, ArrayValues);
    if (!proto[TO_STRING_TAG]) hide(proto, TO_STRING_TAG, NAME);
    Iterators[NAME] = ArrayValues;
    if (explicit) for (key in $iterators) if (!proto[key]) redefine(proto, key, $iterators[key], true);
  }
}


/***/ }),
/* 75 */,
/* 76 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
async function timer(time = 0) {
  await new Promise(resolve => {
    setTimeout(resolve, time);
  });
}

/* harmony default export */ __webpack_exports__["a"] = (timer);

/***/ }),
/* 77 */
/***/ (function(module, exports, __webpack_require__) {

module.exports = __webpack_require__(32)('native-function-to-string', Function.toString);


/***/ }),
/* 78 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

// https://tc39.github.io/proposal-flatMap/#sec-FlattenIntoArray
var isArray = __webpack_require__(43);
var isObject = __webpack_require__(8);
var toLength = __webpack_require__(38);
var ctx = __webpack_require__(33);
var IS_CONCAT_SPREADABLE = __webpack_require__(6)('isConcatSpreadable');

function flattenIntoArray(target, original, source, sourceLen, start, depth, mapper, thisArg) {
  var targetIndex = start;
  var sourceIndex = 0;
  var mapFn = mapper ? ctx(mapper, thisArg, 3) : false;
  var element, spreadable;

  while (sourceIndex < sourceLen) {
    if (sourceIndex in source) {
      element = mapFn ? mapFn(source[sourceIndex], sourceIndex, original) : source[sourceIndex];

      spreadable = false;
      if (isObject(element)) {
        spreadable = element[IS_CONCAT_SPREADABLE];
        spreadable = spreadable !== undefined ? !!spreadable : isArray(element);
      }

      if (spreadable && depth > 0) {
        targetIndex = flattenIntoArray(target, original, element, toLength(element.length), targetIndex, depth - 1) - 1;
      } else {
        if (targetIndex >= 0x1fffffffffffff) throw TypeError();
        target[targetIndex] = element;
      }

      targetIndex++;
    }
    sourceIndex++;
  }
  return targetIndex;
}

module.exports = flattenIntoArray;


/***/ }),
/* 79 */
/***/ (function(module, exports, __webpack_require__) {

// 9.4.2.3 ArraySpeciesCreate(originalArray, length)
var speciesConstructor = __webpack_require__(80);

module.exports = function (original, length) {
  return new (speciesConstructor(original))(length);
};


/***/ }),
/* 80 */
/***/ (function(module, exports, __webpack_require__) {

var isObject = __webpack_require__(8);
var isArray = __webpack_require__(43);
var SPECIES = __webpack_require__(6)('species');

module.exports = function (original) {
  var C;
  if (isArray(original)) {
    C = original.constructor;
    // cross-realm fallback
    if (typeof C == 'function' && (C === Array || isArray(C.prototype))) C = undefined;
    if (isObject(C)) {
      C = C[SPECIES];
      if (C === null) C = undefined;
    }
  } return C === undefined ? Array : C;
};


/***/ }),
/* 81 */
/***/ (function(module, exports) {

module.exports = function (done, value) {
  return { value: value, done: !!done };
};


/***/ }),
/* 82 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var LIBRARY = __webpack_require__(21);
var $export = __webpack_require__(2);
var redefine = __webpack_require__(30);
var hide = __webpack_require__(13);
var Iterators = __webpack_require__(40);
var $iterCreate = __webpack_require__(83);
var setToStringTag = __webpack_require__(45);
var getPrototypeOf = __webpack_require__(35);
var ITERATOR = __webpack_require__(6)('iterator');
var BUGGY = !([].keys && 'next' in [].keys()); // Safari has buggy iterators w/o `next`
var FF_ITERATOR = '@@iterator';
var KEYS = 'keys';
var VALUES = 'values';

var returnThis = function () { return this; };

module.exports = function (Base, NAME, Constructor, next, DEFAULT, IS_SET, FORCED) {
  $iterCreate(Constructor, NAME, next);
  var getMethod = function (kind) {
    if (!BUGGY && kind in proto) return proto[kind];
    switch (kind) {
      case KEYS: return function keys() { return new Constructor(this, kind); };
      case VALUES: return function values() { return new Constructor(this, kind); };
    } return function entries() { return new Constructor(this, kind); };
  };
  var TAG = NAME + ' Iterator';
  var DEF_VALUES = DEFAULT == VALUES;
  var VALUES_BUG = false;
  var proto = Base.prototype;
  var $native = proto[ITERATOR] || proto[FF_ITERATOR] || DEFAULT && proto[DEFAULT];
  var $default = $native || getMethod(DEFAULT);
  var $entries = DEFAULT ? !DEF_VALUES ? $default : getMethod('entries') : undefined;
  var $anyNative = NAME == 'Array' ? proto.entries || $native : $native;
  var methods, key, IteratorPrototype;
  // Fix native
  if ($anyNative) {
    IteratorPrototype = getPrototypeOf($anyNative.call(new Base()));
    if (IteratorPrototype !== Object.prototype && IteratorPrototype.next) {
      // Set @@toStringTag to native iterators
      setToStringTag(IteratorPrototype, TAG, true);
      // fix for some old engines
      if (!LIBRARY && typeof IteratorPrototype[ITERATOR] != 'function') hide(IteratorPrototype, ITERATOR, returnThis);
    }
  }
  // fix Array#{values, @@iterator}.name in V8 / FF
  if (DEF_VALUES && $native && $native.name !== VALUES) {
    VALUES_BUG = true;
    $default = function values() { return $native.call(this); };
  }
  // Define iterator
  if ((!LIBRARY || FORCED) && (BUGGY || VALUES_BUG || !proto[ITERATOR])) {
    hide(proto, ITERATOR, $default);
  }
  // Plug for library
  Iterators[NAME] = $default;
  Iterators[TAG] = returnThis;
  if (DEFAULT) {
    methods = {
      values: DEF_VALUES ? $default : getMethod(VALUES),
      keys: IS_SET ? $default : getMethod(KEYS),
      entries: $entries
    };
    if (FORCED) for (key in methods) {
      if (!(key in proto)) redefine(proto, key, methods[key]);
    } else $export($export.P + $export.F * (BUGGY || VALUES_BUG), NAME, methods);
  }
  return methods;
};


/***/ }),
/* 83 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var create = __webpack_require__(48);
var descriptor = __webpack_require__(29);
var setToStringTag = __webpack_require__(45);
var IteratorPrototype = {};

// 25.1.2.1.1 %IteratorPrototype%[@@iterator]()
__webpack_require__(13)(IteratorPrototype, __webpack_require__(6)('iterator'), function () { return this; });

module.exports = function (Constructor, NAME, next) {
  Constructor.prototype = create(IteratorPrototype, { next: descriptor(1, next) });
  setToStringTag(Constructor, NAME + ' Iterator');
};


/***/ }),
/* 84 */
/***/ (function(module, exports, __webpack_require__) {

// false -> Array#indexOf
// true  -> Array#includes
var toIObject = __webpack_require__(14);
var toLength = __webpack_require__(38);
var toAbsoluteIndex = __webpack_require__(85);
module.exports = function (IS_INCLUDES) {
  return function ($this, el, fromIndex) {
    var O = toIObject($this);
    var length = toLength(O.length);
    var index = toAbsoluteIndex(fromIndex, length);
    var value;
    // Array#includes uses SameValueZero equality algorithm
    // eslint-disable-next-line no-self-compare
    if (IS_INCLUDES && el != el) while (length > index) {
      value = O[index++];
      // eslint-disable-next-line no-self-compare
      if (value != value) return true;
    // Array#indexOf ignores holes, Array#includes - not
    } else for (;length > index; index++) if (IS_INCLUDES || index in O) {
      if (O[index] === el) return IS_INCLUDES || index || 0;
    } return !IS_INCLUDES && -1;
  };
};


/***/ }),
/* 85 */
/***/ (function(module, exports, __webpack_require__) {

var toInteger = __webpack_require__(51);
var max = Math.max;
var min = Math.min;
module.exports = function (index, length) {
  index = toInteger(index);
  return index < 0 ? max(index + length, 0) : min(index, length);
};


/***/ }),
/* 86 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var fails = __webpack_require__(11);

module.exports = function (method, arg) {
  return !!method && fails(function () {
    // eslint-disable-next-line no-useless-call
    arg ? method.call(null, function () { /* empty */ }, 1) : method.call(null);
  });
};


/***/ }),
/* 87 */
/***/ (function(module, exports, __webpack_require__) {

// 7.3.20 SpeciesConstructor(O, defaultConstructor)
var anObject = __webpack_require__(17);
var aFunction = __webpack_require__(12);
var SPECIES = __webpack_require__(6)('species');
module.exports = function (O, D) {
  var C = anObject(O).constructor;
  var S;
  return C === undefined || (S = anObject(C)[SPECIES]) == undefined ? D : aFunction(S);
};


/***/ }),
/* 88 */
/***/ (function(module, exports, __webpack_require__) {

var anObject = __webpack_require__(17);
var isObject = __webpack_require__(8);
var newPromiseCapability = __webpack_require__(89);

module.exports = function (C, x) {
  anObject(C);
  if (isObject(x) && x.constructor === C) return x;
  var promiseCapability = newPromiseCapability.f(C);
  var resolve = promiseCapability.resolve;
  resolve(x);
  return promiseCapability.promise;
};


/***/ }),
/* 89 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

// 25.4.1.5 NewPromiseCapability(C)
var aFunction = __webpack_require__(12);

function PromiseCapability(C) {
  var resolve, reject;
  this.promise = new C(function ($$resolve, $$reject) {
    if (resolve !== undefined || reject !== undefined) throw TypeError('Bad Promise constructor');
    resolve = $$resolve;
    reject = $$reject;
  });
  this.resolve = aFunction(resolve);
  this.reject = aFunction(reject);
}

module.exports.f = function (C) {
  return new PromiseCapability(C);
};


/***/ }),
/* 90 */
/***/ (function(module, exports) {

module.exports = '\x09\x0A\x0B\x0C\x0D\x20\xA0\u1680\u180E\u2000\u2001\u2002\u2003' +
  '\u2004\u2005\u2006\u2007\u2008\u2009\u200A\u202F\u205F\u3000\u2028\u2029\uFEFF';


/***/ }),
/* 91 */
/***/ (function(module, exports, __webpack_require__) {

var global = __webpack_require__(3);
var navigator = global.navigator;

module.exports = navigator && navigator.userAgent || '';


/***/ }),
/* 92 */
/***/ (function(module, exports, __webpack_require__) {

var ctx = __webpack_require__(33);
var invoke = __webpack_require__(93);
var html = __webpack_require__(53);
var cel = __webpack_require__(37);
var global = __webpack_require__(3);
var process = global.process;
var setTask = global.setImmediate;
var clearTask = global.clearImmediate;
var MessageChannel = global.MessageChannel;
var Dispatch = global.Dispatch;
var counter = 0;
var queue = {};
var ONREADYSTATECHANGE = 'onreadystatechange';
var defer, channel, port;
var run = function () {
  var id = +this;
  // eslint-disable-next-line no-prototype-builtins
  if (queue.hasOwnProperty(id)) {
    var fn = queue[id];
    delete queue[id];
    fn();
  }
};
var listener = function (event) {
  run.call(event.data);
};
// Node.js 0.9+ & IE10+ has setImmediate, otherwise:
if (!setTask || !clearTask) {
  setTask = function setImmediate(fn) {
    var args = [];
    var i = 1;
    while (arguments.length > i) args.push(arguments[i++]);
    queue[++counter] = function () {
      // eslint-disable-next-line no-new-func
      invoke(typeof fn == 'function' ? fn : Function(fn), args);
    };
    defer(counter);
    return counter;
  };
  clearTask = function clearImmediate(id) {
    delete queue[id];
  };
  // Node.js 0.8-
  if (__webpack_require__(34)(process) == 'process') {
    defer = function (id) {
      process.nextTick(ctx(run, id, 1));
    };
  // Sphere (JS game engine) Dispatch API
  } else if (Dispatch && Dispatch.now) {
    defer = function (id) {
      Dispatch.now(ctx(run, id, 1));
    };
  // Browsers with MessageChannel, includes WebWorkers
  } else if (MessageChannel) {
    channel = new MessageChannel();
    port = channel.port2;
    channel.port1.onmessage = listener;
    defer = ctx(port.postMessage, port, 1);
  // Browsers with postMessage, skip WebWorkers
  // IE8 has postMessage, but it's sync & typeof its postMessage is 'object'
  } else if (global.addEventListener && typeof postMessage == 'function' && !global.importScripts) {
    defer = function (id) {
      global.postMessage(id + '', '*');
    };
    global.addEventListener('message', listener, false);
  // IE8-
  } else if (ONREADYSTATECHANGE in cel('script')) {
    defer = function (id) {
      html.appendChild(cel('script'))[ONREADYSTATECHANGE] = function () {
        html.removeChild(this);
        run.call(id);
      };
    };
  // Rest old browsers
  } else {
    defer = function (id) {
      setTimeout(ctx(run, id, 1), 0);
    };
  }
}
module.exports = {
  set: setTask,
  clear: clearTask
};


/***/ }),
/* 93 */
/***/ (function(module, exports) {

// fast apply, http://jsperf.lnkit.com/fast-apply/5
module.exports = function (fn, args, that) {
  var un = that === undefined;
  switch (args.length) {
    case 0: return un ? fn()
                      : fn.call(that);
    case 1: return un ? fn(args[0])
                      : fn.call(that, args[0]);
    case 2: return un ? fn(args[0], args[1])
                      : fn.call(that, args[0], args[1]);
    case 3: return un ? fn(args[0], args[1], args[2])
                      : fn.call(that, args[0], args[1], args[2]);
    case 4: return un ? fn(args[0], args[1], args[2], args[3])
                      : fn.call(that, args[0], args[1], args[2], args[3]);
  } return fn.apply(that, args);
};


/***/ }),
/* 94 */
/***/ (function(module, exports, __webpack_require__) {

var META = __webpack_require__(31)('meta');
var isObject = __webpack_require__(8);
var has = __webpack_require__(19);
var setDesc = __webpack_require__(10).f;
var id = 0;
var isExtensible = Object.isExtensible || function () {
  return true;
};
var FREEZE = !__webpack_require__(11)(function () {
  return isExtensible(Object.preventExtensions({}));
});
var setMeta = function (it) {
  setDesc(it, META, { value: {
    i: 'O' + ++id, // object ID
    w: {}          // weak collections IDs
  } });
};
var fastKey = function (it, create) {
  // return primitive with prefix
  if (!isObject(it)) return typeof it == 'symbol' ? it : (typeof it == 'string' ? 'S' : 'P') + it;
  if (!has(it, META)) {
    // can't set metadata to uncaught frozen object
    if (!isExtensible(it)) return 'F';
    // not necessary to add metadata
    if (!create) return 'E';
    // add missing metadata
    setMeta(it);
  // return object ID
  } return it[META].i;
};
var getWeak = function (it, create) {
  if (!has(it, META)) {
    // can't set metadata to uncaught frozen object
    if (!isExtensible(it)) return true;
    // not necessary to add metadata
    if (!create) return false;
    // add missing metadata
    setMeta(it);
  // return hash weak collections IDs
  } return it[META].w;
};
// add metadata on freeze-family methods calling
var onFreeze = function (it) {
  if (FREEZE && meta.NEED && isExtensible(it) && !has(it, META)) setMeta(it);
  return it;
};
var meta = module.exports = {
  KEY: META,
  NEED: false,
  fastKey: fastKey,
  getWeak: getWeak,
  onFreeze: onFreeze
};


/***/ }),
/* 95 */
/***/ (function(module, exports) {

exports.f = Object.getOwnPropertySymbols;


/***/ }),
/* 96 */,
/* 97 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return byLatency; });
const ERROR = 'ERROR';
const PENDING = 'PENDING';

function byLatency(a, b) {
  if (a < 0) {
    return 1;
  }

  if (b < 0) {
    return -1;
  }

  if (a === ERROR) {
    return 1;
  }

  if (b === ERROR) {
    return -1;
  }

  if (a === PENDING) {
    return 1;
  }

  if (b === PENDING) {
    return -1;
  }

  return a - b;
}



/***/ }),
/* 98 */,
/* 99 */,
/* 100 */,
/* 101 */
/***/ (function(module, exports, __webpack_require__) {

// 19.1.2.7 / 15.2.3.4 Object.getOwnPropertyNames(O)
var $keys = __webpack_require__(61);
var hiddenKeys = __webpack_require__(44).concat('length', 'prototype');

exports.f = Object.getOwnPropertyNames || function getOwnPropertyNames(O) {
  return $keys(O, hiddenKeys);
};


/***/ }),
/* 102 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/**
 * determine if extension running in devmode or not
 *
 * @return {boolean}
 */
function isDev() {
  return "production" === 'development';
}

/* harmony default export */ __webpack_exports__["a"] = (isDev);

/***/ }),
/* 103 */,
/* 104 */
/***/ (function(module, exports, __webpack_require__) {

/* eslint-disable
    default-case,
    func-names,
    no-restricted-syntax,
    no-underscore-dangle,
*/
const config = __webpack_require__(107);

const util = __webpack_require__(109);

const engine = __webpack_require__(146);

const log = __webpack_require__(108);

const {
  classof
} = __webpack_require__(147);
/*
  Helper functions and exports
*/
// We need to jump through some hoops in order to stringify the engine correctly


const serializeEngineToString = function (e) {
  e = e || engine;
  const res = [];

  for (const k of Object.keys(e)) {
    const v = e[k];
    const strV = v.toString();

    switch (typeof e[k]) {
      // We need to serialize different property types differently.
      case 'function':
        strV.startsWith('function') ? res.push(`${k}: ${strV}`) : res.push(`${k}: function ${strV}`);
        break;

      case 'object':
        res.push(`${k}: ${JSON.stringify(e[k])}`);
        break;
    }
  }

  return `{ ${res.join(',')} }`; // Wrap engine contents in object literal
}; // NOTE: Regexp don't survive JSON.stringify correctly
// See: http://stackoverflow.com/questions/12075927/serialization-of-regexp
// We have to issue toString() on them when exporting and not put them in quotes.


const pacScriptRegexp = `\
e.data.IPv4NotationRE = ${engine.data.IPv4NotationRE.toString()};
e.data.localIPsRE = ${engine.data.localIPsRE.toString()};\
`; // Export complete stringified proxy.pac
// The pac script needs to be self-contained as it cannot access outside data.
// NOTE: You can eval and test the behaviour in your console using this:

exports.exportPAC = function (defaultLocation, nodeDict, rules, pageExcludes) {
  rules = rules || [];
  pageExcludes = pageExcludes || [];
  log.debug('pacengine.exportPAC', {
    defaultLocation,
    nodeDict,
    rules,
    pageExcludes
  });
  const pac = `\
/*Private Internet Access*/
function FindProxyForURL(url, host) {
  var e = ${serializeEngineToString()};
  e.data.localDomains = e.data.localDomains.concat(${JSON.stringify(pageExcludes)});
  ${pacScriptRegexp}

  e.data.defaultLocation = '${defaultLocation}';
  e.data.nodeDict = ${JSON.stringify(nodeDict)};
  e.data.rulesWithOverrides = ${JSON.stringify(engine.mergeRuleOverrides(rules, config.get().ruleOverrides))};

  var res = e._getProxyState(url, host, e.data.rulesWithOverrides);
  var cc;
  if (res === 'LOCAL' || res === 'DIRECT' || res === 'OFF') {return 'DIRECT'};
  if (res === 'DEFAULT') {cc = e.data.defaultLocation} else {cc = res};
  var override = e.matchNodeOverride(host, cc);
  if (override) {cc = override};
  return e.nodeLookup(e.data.nodeDict, cc) || 'DIRECT';
}\
`;
  return pac;
}; // Returns LOCAL, DIRECT, DEFAULT or $COUNTRYCODE for a given URL and host.
// $COUNTRYCODE (can be "OFF") is only being returned if a custom rule did match.
// Meant for internal consumption to communicate proxy state to the user.


exports.getProxyStateByURL = function (url, host, rules) {
  rules = rules || [];
  host = host || util.parseURL(url).host || url;
  return engine._getProxyState(url, host, rules);
}; // Returns a lookup dictionary with country codes and respective concatenated proxy nodes.
// e.g. {"GB":"HTTPS 8.8.8.8:443;HTTPS 8.8.8.9:443","US":"HTTPS 2.2.2.2:443"}
// parameter noExtras removes the HTTPS and port appendix


exports.getNodeDictFromLocations = function (locations, key) {
  const nodeDict = {};
  locations.map(node => {
    const {
      host,
      id
    } = node;
    const port = node[key];
    nodeDict[id] = typeof browser == 'undefined' ? `HTTPS ${host}:${port}` : `${host}:${port}`;
  });
  return nodeDict;
};

exports.matchRules = (rules, host, url) => engine.matchRules(rules, host, url);

/***/ }),
/* 105 */,
/* 106 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var _helpers_applyListener__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(22);
/*
  *** WARNING ***
  This event handler is always active. It could be run while a direct connection is being
  used, while another proxy extension is active, or while the Private Internet Access
  extension is active.

  Being unaware of this could introduce serious bugs that compromise the security of the
  extension.

*/


function onError(app) {
  const basename = filename => {
    return filename.split('/').slice(-1);
  };

  return e => {
    const {
      filename,
      lineno,
      message
    } = e; // NOTE: This will catch any 'dead object' asynchronous bugs while the view is hanging.

    try {
      app.logger.debug(`javascript error at ${basename(filename)}:${lineno}: ${message}`);
    } catch (err) {
      // eslint-disable-next-line no-console
      console.log(err);
    }
  };
}

/* harmony default export */ __webpack_exports__["a"] = (Object(_helpers_applyListener__WEBPACK_IMPORTED_MODULE_0__[/* default */ "a"])((app, addListener) => {
  addListener(onError(app));
}));

/***/ }),
/* 107 */
/***/ (function(module, exports, __webpack_require__) {

// Built-in config
const log = __webpack_require__(108);

const config = {
  connectionCheckDomains: [{
    url: 'http://www.google.com.sg/gen_204',
    code: 204
  }, {
    url: 'http://g.cn/generate_204',
    code: 204
  }, {
    url: 'http://www.thinkdifferent.us',
    code: 200
  }, {
    url: 'http://www.airport.us',
    code: 200
  }, {
    url: 'http://detectportal.firefox.com/success.txt',
    code: 200
  }, {
    url: 'http://captive.apple.com',
    code: 200
  }],
  localDomains: [// Our domains
  'd1jr1idae5ms9n.cloudfront.net', // Local network
  'local', // .local are often employed in private networks
  'ip', // speedport.ip is being used by telekom routers
  'fritz.box', // FRITZ!Box router settings
  'kabel.box', // Vodafone router settings
  'invalid', // https://en.wikipedia.org/wiki/.invalid
  'intra', // used by some companies for local intranet
  'intranet', // used by some companies for local intranet
  'test', // https://en.wikipedia.org/wiki/.test
  'example', // https://en.wikipedia.org/wiki/.example
  'localhost', // https://en.wikipedia.org/wiki/.localhost
  // Misc
  'onion', // Tor domains
  'i2p', // i2p domains
  // DNS that resolves to 127.0.0.1 (mostly for developers)
  'lvh.me', 'vcap.me', '127.0.0.1.xip.io', // http://xip.io/
  'localtest.me', // http://readme.localtest.me/
  // Firefox local pages
  'about:addons', 'about:newtab', 'about:preferences', 'about:config', 'about:debugging'],
  // we need this list to inform the user about conflicting extensions
  blackList: {
    'jid1-4P0kohSJxU1qGg@jetpack': 'hola'
  },
  // This could come out of the API eventually
  alternativeNodes: [],
  // For some hosts it might be required to use alternative servers
  // Previously this only applies to hulu as they blocked the whole Leaseweb US DC.
  nodeOverrides: [],
  // In order to behave like the user would expect we use a ruleOverride list.
  // We're not able to have "tab based" proxy rules but rather host based rules.
  // If the user defines facebook.com in a rule he would expect to unblock all of Facebook,
  // unfortunately that's not the case as FB is using a multitude of additonal hosts for their service.
  // The following list is currently used only internally and not exposed to the user,
  // we might choose to expose this list later on to user editing when we advance the rule feature.
  ruleOverrides: [{
    domains: ['facebook.com'],
    hosts: ['facebook.net', 'fbcdn.com', 'fbcdn.net', 'fbsbx.com', 'fb.me', 'fb.com', 'fbsbx.com.online-metrix.net', 'fbstatic-a.akamaihd.net', 'fbcdn-dragon-a.akamaihd.net']
  }, {
    domains: ['netflix.com'],
    hosts: ['nflxvideo.net']
  }, {
    domains: ['bbc.co.uk', 'bbc.com'],
    hosts: ['bbc.co.uk', 'bbc.com', 'vod-dash-uk-live.akamaized.net', 'vod-thumb-uk-live.akamaized.net']
  }, {
    domains: ['speedtest.net'],
    hosts: ['ooklaserver.net']
  }, {
    domains: ['speedtest.xfinity.com'],
    hosts: ['comcast.net']
  }],
  // The following is a list of hosts for each of which we will close any tab
  // that tries to open a URL with that host
  blockedSites: ['appnord.xyz'],
  // For fixed_servers' bypassList and is taken from
  privateNetworks: ['0.0.0.0/8', '10.0.0.0/8', '127.0.0.0/8', '169.254.0.0/16', '192.168.0.0/16', '172.16.0.0/12', '::1', 'localhost', '*.local']
}; // expose config to the console

if (typeof window !== 'undefined') {
  window.config = config;
}

module.exports = {
  get() {
    return config;
  }

};

/***/ }),
/* 108 */
/***/ (function(module, exports, __webpack_require__) {

var __WEBPACK_AMD_DEFINE_FACTORY__, __WEBPACK_AMD_DEFINE_RESULT__;/*
* loglevel - https://github.com/pimterry/loglevel
*
* Copyright (c) 2013 Tim Perry
* Licensed under the MIT license.
*/
(function (root, definition) {
    "use strict";
    if (true) {
        !(__WEBPACK_AMD_DEFINE_FACTORY__ = (definition),
				__WEBPACK_AMD_DEFINE_RESULT__ = (typeof __WEBPACK_AMD_DEFINE_FACTORY__ === 'function' ?
				(__WEBPACK_AMD_DEFINE_FACTORY__.call(exports, __webpack_require__, exports, module)) :
				__WEBPACK_AMD_DEFINE_FACTORY__),
				__WEBPACK_AMD_DEFINE_RESULT__ !== undefined && (module.exports = __WEBPACK_AMD_DEFINE_RESULT__));
    } else {}
}(this, function () {
    "use strict";

    // Slightly dubious tricks to cut down minimized file size
    var noop = function() {};
    var undefinedType = "undefined";
    var isIE = (typeof window !== undefinedType) && (typeof window.navigator !== undefinedType) && (
        /Trident\/|MSIE /.test(window.navigator.userAgent)
    );

    var logMethods = [
        "trace",
        "debug",
        "info",
        "warn",
        "error"
    ];

    // Cross-browser bind equivalent that works at least back to IE6
    function bindMethod(obj, methodName) {
        var method = obj[methodName];
        if (typeof method.bind === 'function') {
            return method.bind(obj);
        } else {
            try {
                return Function.prototype.bind.call(method, obj);
            } catch (e) {
                // Missing bind shim or IE8 + Modernizr, fallback to wrapping
                return function() {
                    return Function.prototype.apply.apply(method, [obj, arguments]);
                };
            }
        }
    }

    // Trace() doesn't print the message in IE, so for that case we need to wrap it
    function traceForIE() {
        if (console.log) {
            if (console.log.apply) {
                console.log.apply(console, arguments);
            } else {
                // In old IE, native console methods themselves don't have apply().
                Function.prototype.apply.apply(console.log, [console, arguments]);
            }
        }
        if (console.trace) console.trace();
    }

    // Build the best logging method possible for this env
    // Wherever possible we want to bind, not wrap, to preserve stack traces
    function realMethod(methodName) {
        if (methodName === 'debug') {
            methodName = 'log';
        }

        if (typeof console === undefinedType) {
            return false; // No method possible, for now - fixed later by enableLoggingWhenConsoleArrives
        } else if (methodName === 'trace' && isIE) {
            return traceForIE;
        } else if (console[methodName] !== undefined) {
            return bindMethod(console, methodName);
        } else if (console.log !== undefined) {
            return bindMethod(console, 'log');
        } else {
            return noop;
        }
    }

    // These private functions always need `this` to be set properly

    function replaceLoggingMethods(level, loggerName) {
        /*jshint validthis:true */
        for (var i = 0; i < logMethods.length; i++) {
            var methodName = logMethods[i];
            this[methodName] = (i < level) ?
                noop :
                this.methodFactory(methodName, level, loggerName);
        }

        // Define log.log as an alias for log.debug
        this.log = this.debug;
    }

    // In old IE versions, the console isn't present until you first open it.
    // We build realMethod() replacements here that regenerate logging methods
    function enableLoggingWhenConsoleArrives(methodName, level, loggerName) {
        return function () {
            if (typeof console !== undefinedType) {
                replaceLoggingMethods.call(this, level, loggerName);
                this[methodName].apply(this, arguments);
            }
        };
    }

    // By default, we use closely bound real methods wherever possible, and
    // otherwise we wait for a console to appear, and then try again.
    function defaultMethodFactory(methodName, level, loggerName) {
        /*jshint validthis:true */
        return realMethod(methodName) ||
               enableLoggingWhenConsoleArrives.apply(this, arguments);
    }

    function Logger(name, defaultLevel, factory) {
      var self = this;
      var currentLevel;

      var storageKey = "loglevel";
      if (typeof name === "string") {
        storageKey += ":" + name;
      } else if (typeof name === "symbol") {
        storageKey = undefined;
      }

      function persistLevelIfPossible(levelNum) {
          var levelName = (logMethods[levelNum] || 'silent').toUpperCase();

          if (typeof window === undefinedType || !storageKey) return;

          // Use localStorage if available
          try {
              window.localStorage[storageKey] = levelName;
              return;
          } catch (ignore) {}

          // Use session cookie as fallback
          try {
              window.document.cookie =
                encodeURIComponent(storageKey) + "=" + levelName + ";";
          } catch (ignore) {}
      }

      function getPersistedLevel() {
          var storedLevel;

          if (typeof window === undefinedType || !storageKey) return;

          try {
              storedLevel = window.localStorage[storageKey];
          } catch (ignore) {}

          // Fallback to cookies if local storage gives us nothing
          if (typeof storedLevel === undefinedType) {
              try {
                  var cookie = window.document.cookie;
                  var location = cookie.indexOf(
                      encodeURIComponent(storageKey) + "=");
                  if (location !== -1) {
                      storedLevel = /^([^;]+)/.exec(cookie.slice(location))[1];
                  }
              } catch (ignore) {}
          }

          // If the stored level is not valid, treat it as if nothing was stored.
          if (self.levels[storedLevel] === undefined) {
              storedLevel = undefined;
          }

          return storedLevel;
      }

      /*
       *
       * Public logger API - see https://github.com/pimterry/loglevel for details
       *
       */

      self.name = name;

      self.levels = { "TRACE": 0, "DEBUG": 1, "INFO": 2, "WARN": 3,
          "ERROR": 4, "SILENT": 5};

      self.methodFactory = factory || defaultMethodFactory;

      self.getLevel = function () {
          return currentLevel;
      };

      self.setLevel = function (level, persist) {
          if (typeof level === "string" && self.levels[level.toUpperCase()] !== undefined) {
              level = self.levels[level.toUpperCase()];
          }
          if (typeof level === "number" && level >= 0 && level <= self.levels.SILENT) {
              currentLevel = level;
              if (persist !== false) {  // defaults to true
                  persistLevelIfPossible(level);
              }
              replaceLoggingMethods.call(self, level, name);
              if (typeof console === undefinedType && level < self.levels.SILENT) {
                  return "No console available for logging";
              }
          } else {
              throw "log.setLevel() called with invalid level: " + level;
          }
      };

      self.setDefaultLevel = function (level) {
          if (!getPersistedLevel()) {
              self.setLevel(level, false);
          }
      };

      self.enableAll = function(persist) {
          self.setLevel(self.levels.TRACE, persist);
      };

      self.disableAll = function(persist) {
          self.setLevel(self.levels.SILENT, persist);
      };

      // Initialize with the right level
      var initialLevel = getPersistedLevel();
      if (initialLevel == null) {
          initialLevel = defaultLevel == null ? "WARN" : defaultLevel;
      }
      self.setLevel(initialLevel, false);
    }

    /*
     *
     * Top-level API
     *
     */

    var defaultLogger = new Logger();

    var _loggersByName = {};
    defaultLogger.getLogger = function getLogger(name) {
        if ((typeof name !== "symbol" && typeof name !== "string") || name === "") {
          throw new TypeError("You must supply a name when creating a logger.");
        }

        var logger = _loggersByName[name];
        if (!logger) {
          logger = _loggersByName[name] = new Logger(
            name, defaultLogger.getLevel(), defaultLogger.methodFactory);
        }
        return logger;
    };

    // Grab the current global log variable in case of overwrite
    var _log = (typeof window !== undefinedType) ? window.log : undefined;
    defaultLogger.noConflict = function() {
        if (typeof window !== undefinedType &&
               window.log === defaultLogger) {
            window.log = _log;
        }

        return defaultLogger;
    };

    defaultLogger.getLoggers = function getLoggers() {
        return _loggersByName;
    };

    // ES6 default export, for compatibility
    defaultLogger['default'] = defaultLogger;

    return defaultLogger;
}));


/***/ }),
/* 109 */
/***/ (function(module, exports) {

/* eslint-disable
    func-names,
    no-bitwise,
    no-cond-assign,
    no-plusplus,
    no-useless-escape,
*/
exports.generateInstallId = function () {
  const S4 = () => ((1 + Math.random()) * 0x10000 | 0).toString(16).substring(1);

  return `${S4() + S4()}-${S4()}-${S4()}-${S4()}-${S4()}${S4()}${S4()}`;
};

exports.parseURL = function (url) {
  let needle;
  const urlNotation = /^([^:]+):\/\/([^\/:]*)(?::([\d]+))?(?:(\/[^#]*)(?:#(.*))?)?$/i;
  const match = url.match(urlNotation);

  if (!match) {
    return {};
  }

  return {
    scheme: match[1].toLowerCase(),
    host: match[2].toLowerCase(),
    port: match[3],
    path: match[4] || '/',
    fragment: match[5],
    local: (needle = match[1].toLowerCase(), !['http', 'https'].includes(needle))
  };
}; // Fetch and concatenate all utm_* parameters from a given URL


exports.getUTMSourcesFromURL = function (url) {
  let match;
  const {
    path
  } = exports.parseURL(url);
  const search = /[?&]([^=#]+)=([^&#]*)/g;
  const utmParams = [];

  while (match = search.exec(path)) {
    // We push all parameters (key=value) that start with utm_ to an array
    if (match[1].indexOf('utm_') === 0) {
      utmParams.push(`${match[1]}=${match[2]}`);
    }
  }

  return utmParams.join(';'); // Concatenate array to string
}; // Concatenates two arrays with de-duplication
// See: http://stackoverflow.com/a/24072887


exports.concatUnique = (a, b) => a.concat(b).filter((x, i, c) => c.indexOf(x) === i); // "YYYY-MM-DD HH:mm:ss [UTC]" is the format of the dates
// but it also works with another formats :)


exports.parseDate = function (s) {
  const date = new Date(s);

  if (isNaN(date.getTime())) {
    const [dateString, timeString] = s.split(' ');
    const dateParts = dateString.split('-');
    const timeParts = timeString.split(':');
    return new Date(dateParts[0], dateParts[1] - 1, dateParts[2], timeParts[0], timeParts[1], timeParts[2]);
  }

  return date;
}; // Shuffles the array with the Fisher-Yates algorithm (!!! not pure by design)


exports.shuffle = function (things) {
  let currIndex = things.length;
  let tmpVal = null;
  let randomIndex = null;

  while (currIndex !== 0) {
    randomIndex = Math.floor(Math.random() * currIndex);
    currIndex--;
    tmpVal = things[currIndex];
    things[currIndex] = things[randomIndex];
    things[randomIndex] = tmpVal;
  }

  return things;
}; // Chunks the array


exports.chunk = function (arr, len) {
  len = len <= 0 ? 1 : len;
  const chunks = [];
  let i = 0;
  const n = arr.length;

  while (i < n) {
    chunks.push(arr.slice(i, i += len));
  }

  return chunks;
}; // Praise stackoverflow.com! (and Java™)


exports.hashCode = val => {
  let hash = 0;

  if (!(typeof val === 'string')) {
    val = JSON.stringify(val);
  }

  if (!val || val.length === 0) {
    return hash;
  }

  for (let i = 0; i < val.length; i++) {
    const char = val.charCodeAt(i);
    hash = (hash << 5) - hash + char;
    hash &= hash; // Convert to 32bit integer
  }

  return hash;
};

exports.hashString = val => exports.hashCode(val).toString();

/***/ }),
/* 110 */
/***/ (function(module, exports, __webpack_require__) {

// fallback for IE11 buggy Object.getOwnPropertyNames with iframe and window
var toIObject = __webpack_require__(14);
var gOPN = __webpack_require__(101).f;
var toString = {}.toString;

var windowNames = typeof window == 'object' && window && Object.getOwnPropertyNames
  ? Object.getOwnPropertyNames(window) : [];

var getWindowNames = function (it) {
  try {
    return gOPN(it);
  } catch (e) {
    return windowNames.slice();
  }
};

module.exports.f = function getOwnPropertyNames(it) {
  return windowNames && toString.call(it) == '[object Window]' ? getWindowNames(it) : gOPN(toIObject(it));
};


/***/ }),
/* 111 */
/***/ (function(module, exports, __webpack_require__) {

// getting tag from 19.1.3.6 Object.prototype.toString()
var cof = __webpack_require__(34);
var TAG = __webpack_require__(6)('toStringTag');
// ES3 wrong here
var ARG = cof(function () { return arguments; }()) == 'Arguments';

// fallback for IE11 Script Access Denied error
var tryGet = function (it, key) {
  try {
    return it[key];
  } catch (e) { /* empty */ }
};

module.exports = function (it) {
  var O, T, B;
  return it === undefined ? 'Undefined' : it === null ? 'Null'
    // @@toStringTag case
    : typeof (T = tryGet(O = Object(it), TAG)) == 'string' ? T
    // builtinTag case
    : ARG ? cof(O)
    // ES3 arguments fallback
    : (B = cof(O)) == 'Object' && typeof O.callee == 'function' ? 'Arguments' : B;
};


/***/ }),
/* 112 */
/***/ (function(module, exports, __webpack_require__) {

// all object keys, includes non-enumerable and symbols
var gOPN = __webpack_require__(101);
var gOPS = __webpack_require__(95);
var anObject = __webpack_require__(17);
var Reflect = __webpack_require__(3).Reflect;
module.exports = Reflect && Reflect.ownKeys || function ownKeys(it) {
  var keys = gOPN.f(anObject(it));
  var getSymbols = gOPS.f;
  return getSymbols ? keys.concat(getSymbols(it)) : keys;
};


/***/ }),
/* 113 */
/***/ (function(module, exports, __webpack_require__) {

var DESCRIPTORS = __webpack_require__(5);
var getKeys = __webpack_require__(26);
var toIObject = __webpack_require__(14);
var isEnum = __webpack_require__(42).f;
module.exports = function (isEntries) {
  return function (it) {
    var O = toIObject(it);
    var keys = getKeys(O);
    var length = keys.length;
    var i = 0;
    var result = [];
    var key;
    while (length > i) {
      key = keys[i++];
      if (!DESCRIPTORS || isEnum.call(O, key)) {
        result.push(isEntries ? [key, O[key]] : O[key]);
      }
    }
    return result;
  };
};


/***/ }),
/* 114 */
/***/ (function(module, exports, __webpack_require__) {

var dP = __webpack_require__(10);
var gOPD = __webpack_require__(28);
var ownKeys = __webpack_require__(112);
var toIObject = __webpack_require__(14);

module.exports = function define(target, mixin) {
  var keys = ownKeys(toIObject(mixin));
  var length = keys.length;
  var i = 0;
  var key;
  while (length > i) dP.f(target, key = keys[i++], gOPD.f(mixin, key));
  return target;
};


/***/ }),
/* 115 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
class SameApp {
  constructor(app) {
    this.app = app;
    this.init = this.init.bind(this);
    this.storage = app.util.storage;
    this.returnBrowser = this.returnBrowser.bind(this);
    this.saveToStorage = this.saveToStorage.bind(this);
    this.adapter = app.adapter;
  }

  init() {
    if (typeof browser == "undefined") {
      this.saveToStorage("sameAppBrowser", 'chrome');
    } else {
      this.saveToStorage("sameAppBrowser", 'firefox');
    }
  }

  returnBrowser() {
    const browser = this.storage.getItem("sameAppBrowser");
    return browser;
  }

  saveToStorage(key, value, bridged) {
    if (!bridged && typeof browser != 'undefined') {
      this.adapter.sendMessage('sameApp', {
        settingID: key,
        value: value
      });
    }

    return this.storage.setItem(key, value);
  }

}

/* harmony default export */ __webpack_exports__["a"] = (SameApp);

/***/ }),
/* 116 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var _helpers_http__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(15);

const USERNAME_KEY = 'form:username';
const PASSWORD_KEY = 'form:password';
const LOGGED_IN_KEY = 'loggedIn';
const REMEMBER_ME_KEY = 'rememberme';
const AUTH_TOKEN_KEY = 'authToken';
const AUTH_TIMEOUT = 5000;
const AUTH_ENDPOINT = 'https://www.privateinternetaccess.com/api/client/v2/token';
const ACCOUNT_ENDPOINT = 'https://www.privateinternetaccess.com/api/client/v2/account';
/**
 * Controls user information and authentication in
 * the extension
 */

class User {
  constructor(app, foreground = false) {
    // bindings
    this.getLoggedIn = this.getLoggedIn.bind(this);
    this.setLoggedIn = this.setLoggedIn.bind(this);
    this.getRememberMe = this.getRememberMe.bind(this);
    this.setRememberMe = this.setRememberMe.bind(this);
    this.checkUserName = this.checkUserName.bind(this);
    this.getUsername = this.getUsername.bind(this);
    this.setUsername = this.setUsername.bind(this);
    this.getPassword = this.getPassword.bind(this);
    this.getAuthToken = this.getAuthToken.bind(this);
    this.setAuthToken = this.setAuthToken.bind(this);
    this.setAccount = this.setAccount.bind(this);
    this.updateAccount = this.updateAccount.bind(this);
    this.auth = this.auth.bind(this);
    this.logout = this.logout.bind(this);
    this.init = this.init.bind(this); // init

    this.app = app;
    this.foreground = foreground;
    this.authTimeout = 5000; // handle getting account info from storage

    this.account = undefined;
    const account = this.storage.getItem('account');

    if (account) {
      this.account = account;
    } // get credentials and loggedIn from storage


    const {
      util: {
        storage
      }
    } = app;
    this.username = storage.getItem(USERNAME_KEY) || '';
    this.authToken = storage.getItem(AUTH_TOKEN_KEY) || ''; // init loggedIn, user#setLoggedIn relies on app to be initialized

    this.loggedIn = storage.getItem(LOGGED_IN_KEY) || '';
  }
  /* ------------------------------------ */

  /*              Getters                 */

  /* ------------------------------------ */


  get storage() {
    return this.app.util.storage;
  }

  get adapter() {
    return this.app.adapter;
  }

  get settings() {
    return this.app.util.settings;
  }

  get icon() {
    return this.app.util.icon;
  }

  get proxy() {
    return this.app.proxy;
  }

  async init() {
    const {
      util: {
        storage
      }
    } = this.app;
    const password = storage.getItem(PASSWORD_KEY) || null; // If credentials exists and loggedIn, re-auth using token
    // NOTE: This should be removed after all users are no longer using the old auth system

    if (password && this.username && this.getLoggedIn()) {
      try {
        await this.auth(this.username, password);
      } catch (_) {
        this.setLoggedIn(false);
      }
    } else {
      // call setLoggedIn to setup other modules relying on user
      this.setLoggedIn(this.getLoggedIn());
    } // clear legacy password


    this.password = null;
    storage.removeItem(PASSWORD_KEY);
  }

  getLoggedIn() {
    return this.loggedIn;
  }

  setLoggedIn(value) {
    const {
      app: {
        util: {
          settingsmanager
        }
      }
    } = this;
    this.loggedIn = value;
    this.storage.setItem(LOGGED_IN_KEY, value);

    if (this.foreground && typeof browser != 'undefined') {
      this.adapter.sendMessage('util.user.setLoggedIn', {
        value
      });
    } else {
      if (value) {
        settingsmanager.enable();
      } else {
        settingsmanager.disable();
      }
    }
  }
  /**
   * Get whether or not username & token should be remembered
   */


  getRememberMe() {
    return this.settings.getItem(REMEMBER_ME_KEY);
  }

  setRememberMe(rememberMe) {
    let username = '';

    if (rememberMe) {
      username = this.getUsername();
    } // update username and rememberMe in localStorage


    this.storage.setItem(USERNAME_KEY, username);
    this.settings.setItem(REMEMBER_ME_KEY, Boolean(rememberMe), this.foreground);

    if (this.foreground && typeof browser != 'undefined') {
      this.adapter.sendMessage('util.user.setRememberMe', {
        rememberMe
      });
    }
  }

  checkUserName() {
    if (!this.getRememberMe()) {
      this.username = '';
      this.storage.setItem(USERNAME_KEY, this.username);
    }
  }

  getUsername() {
    return this.username || '';
  }

  setUsername(username) {
    this.username = username.trim();

    if (this.getRememberMe()) {
      this.storage.setItem(USERNAME_KEY, this.username);
    }

    if (this.foreground && typeof browser != 'undefined') {
      this.adapter.sendMessage('util.user.setUsername', {
        username: this.username
      });
    }
  }

  getPassword() {
    return this.password || '';
  }

  getAuthToken() {
    return this.authToken || '';
  }

  setAuthToken(authToken) {
    this.authToken = authToken;
    this.storage.setItem(AUTH_TOKEN_KEY, authToken);

    if (this.foreground && typeof browser != 'undefined') {
      this.adapter.sendMessage('util.user.setAuthToken', {
        authToken
      });
    }
  }

  setAccount(account) {
    if (!account) {
      return;
    }

    this.account = account;
    delete this.account.email;
    this.storage.setItem('account', account);

    if (this.foreground && typeof browser != 'undefined') {
      this.adapter.sendMessage('util.user.setAccount', account);
    }
  }
  /**
   * Update the account information for the user
   */


  updateAccount() {
    debug('user.js: start account info');
    const headers = {
      Authorization: `Token ${this.authToken}`
    };
    return _helpers_http__WEBPACK_IMPORTED_MODULE_0__[/* default */ "a"].get(ACCOUNT_ENDPOINT, {
      headers
    }).then(res => {
      debug('user.js: account info ok');
      return res.json();
    }).then(body => {
      this.setAccount(body);
      return body;
    }).catch(res => {
      debug(`user.js: account info error, ${res.cause}`);
    });
  }
  /**
   * Authenticate with PIA's service
   */


  auth(rawUsername, password) {
    const username = rawUsername.trim();
    const body = JSON.stringify({
      username,
      password
    });
    const headers = {
      'Content-Type': 'application/json'
    };
    const options = {
      headers,
      body,
      timeout: AUTH_TIMEOUT
    };
    return _helpers_http__WEBPACK_IMPORTED_MODULE_0__[/* default */ "a"].post(AUTH_ENDPOINT, options).then(res => {
      return res.json();
    }).then(resBody => {
      // set user as authenticated
      this.setAuthToken(resBody.token);
      this.setLoggedIn(true);
      this.icon.updateTooltip(); // update account information

      this.updateAccount();
      return resBody;
    }).catch(res => {
      this.setLoggedIn(false);
      throw res;
    });
  }

  logout(cb) {
    /* FIXME: remove callback for promise chaining. */
    return this.proxy.disable().then(() => {
      this.setLoggedIn(false);
      this.setAuthToken(null);
      this.icon.updateTooltip();

      if (cb) {
        cb();
      }
    });
  }

}

/* harmony default export */ __webpack_exports__["a"] = (User);

/***/ }),
/* 117 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
const greenRobots = {
  16: '/images/icons/icon16.png',
  32: '/images/icons/icon32.png',
  48: '/images/icons/icon48.png',
  64: '/images/icons/icon64.png',
  128: '/images/icons/icon128.png'
};
const redRobots = {
  16: '/images/icons/icon16red.png',
  32: '/images/icons/icon32red.png',
  48: '/images/icons/icon48red.png',
  64: '/images/icons/icon64red.png',
  128: '/images/icons/icon128red.png'
};

const pacengine = __webpack_require__(104); // const urlParser = require('../pacengine/url-parser');

/**
 * Control the icon used to open the foreground
 *
 * Should show green icon w/ flag when connected, or
 * red icon w/o flag when disconnected
 */


class Icon {
  constructor(app) {
    // bindings
    this.online = this.online.bind(this);
    this.offline = this.offline.bind(this);
    this.updateTooltip = this.updateTooltip.bind(this); // init

    this.app = app;
  }

  getCurrentState(url, parseUrl) {
    const userRulesSmartLoc = this.app.util.smartlocation.getSmartLocationRules('smartLocationRules').map(loc => {
      return {
        cc: loc.proxy.id,
        domain: loc.userRules,
        country: loc
      };
    });
    const rules = typeof browser == 'undefined' ? this.app.proxy.rules : userRulesSmartLoc;
    const state = pacengine.getProxyStateByURL(url, parseUrl.host, rules); // Add booleans indicating the state of a tab.

    const tabState = {
      isDefault: state === 'DEFAULT',
      // Only occurs if no rule did match
      isLocal: state === 'LOCAL',
      // Only true on local sites (including config.localDomains)
      isDirect: state === 'OFF',
      isRuleActive: false,
      customCountry: null
    };
    tabState.isRuleActive = !(tabState.isDefault || tabState.isLocal); // If a rule matches add the country code, make clear it's not a full location by variable naming.

    if (tabState.isRuleActive && !tabState.isDirect) {
      tabState.customCountry = state;
    }

    return tabState;
  }

  async upatedOnChangeTab(tabId) {
    //check if there are rules
    const checkSmartLoc = this.app.util.smartlocation.getSmartLocationRules('checkSmartLocation');
    chrome.tabs.get(tabId, tab => {
      this.app.util.smartlocation.setCurrentDomain();
      this.app.util.regionlist.selectedRegionSmartLoc = null;
      this.online(null);

      if (tab.url) {
        //get the parsed url
        const parseUrl = this.app.helpers.UrlParser.parse(tab.url); //get the state if there are rules

        const tabState = this.getCurrentState(tab.url, parseUrl);

        if (checkSmartLoc) {
          this.app.util.ipManager.updateIpByRegion(tabState); //change icon

          this.getStateAndChangeIcon(tabState);
        }
      }
    });
  }

  getStateAndChangeIcon(tab) {
    //change icon for location
    if (tab.customCountry) {
      const location = this.app.util.regionlist.getRegionById(tab.customCountry);
      this.app.util.regionlist.selectedRegionSmartLoc = location;
      this.online(location);
    }
  }

  async online() {
    const regionSelected = this.app.util.regionlist.getSelectedRegion();
    const imageData = {};
    const imagePromises = [];
    let region = regionSelected ? regionSelected : this.app.util.regionlist.getSelectedRegion();
    Object.keys(greenRobots).forEach(size => {
      imagePromises.push(Icon.generateIcon(imageData, size, region));
    });
    Promise.all(imagePromises).then(() => {
      if (region && this.app.proxy.enabled()) {
        chrome.browserAction.setIcon({
          imageData
        });
        debug('icon.js: set icon online');
        this.updateTooltip();
      } else {
        debug('icon.js: ignore set icon online, not online');
      }
    });
  }

  async offline() {
    const imageData = {};
    const imagePromises = [];
    Object.keys(greenRobots).forEach(size => {
      imagePromises.push(Icon.generateErrorIcon(imageData, size));
    });
    Promise.all(imagePromises).then(() => {
      if (!this.app.proxy.enabled()) {
        chrome.browserAction.setIcon({
          imageData
        });
        debug('icon.js: set icon offline');
        this.updateTooltip();
      } else {
        debug('icon.js: ignore set icon offline, we\'re online');
      }
    });
  }

  updateTooltip(regionIcon = null) {
    let title;
    const {
      proxy,
      buildinfo
    } = this.app;
    const {
      regionlist,
      user
    } = this.app.util;
    const region = regionIcon ? regionIcon : regionlist.getSelectedRegion();

    if (region && proxy.enabled()) {
      title = t('YouAreConnectedTo');
    } else {
      title = user.getLoggedIn() ? t('YouAreNotConnected') : 'Private Internet Access';
    } // Badge


    chrome.browserAction.setTitle({
      title
    });

    const badgeInfo = (() => {
      switch (buildinfo.name) {
        case 'beta':
          return {
            text: buildinfo.name,
            color: '#FF0000'
          };

        case 'dev':
        case 'e2e':
        case 'qa':
          return {
            text: buildinfo.name,
            color: '#0198E1'
          };

        default:
          return null;
      }
    })();

    if (badgeInfo) {
      if (region && proxy.enabled()) {
        chrome.browserAction.setBadgeText({
          text: ''
        });
      } else {
        const {
          text,
          color
        } = badgeInfo;
        chrome.browserAction.setBadgeText({
          text
        });
        chrome.browserAction.setBadgeBackgroundColor({
          color
        });
      }
    }

    debug(`icon.js: tooltip updated`);
  }

  static newCanvasCtx(image) {
    const canvas = document.createElement('canvas');
    canvas.width = image.width;
    canvas.height = image.height;
    return canvas.getContext('2d');
  }

  static newImage(imagePath) {
    return new Promise((resolve, reject) => {
      const image = new Image();
      image.src = imagePath;

      image.onload = () => {
        return resolve(image);
      };

      image.onerror = reject;
    });
  }

  static drawImage(ctx, image, x = 0, y = 0) {
    ctx.drawImage(image, x, y, image.width, image.height);
    return ctx;
  }

  static drawBorder(ctx, map) {
    const {
      width,
      height,
      color,
      lineWidth
    } = map;
    ctx.strokeStyle = color;
    ctx.lineWidth = lineWidth;
    ctx.strokeRect(0, 0, width, height);
  }

  static drawFlagOnto(ctx, flag) {
    const fctx = Icon.drawImage(Icon.newCanvasCtx(flag), flag);
    Icon.drawBorder(fctx, {
      lineWidth: 1,
      height: flag.height,
      width: flag.width,
      color: '#000000'
    });
    const image = fctx.getImageData(0, 0, flag.width, flag.height);
    ctx.putImageData(image, 0, flag.width - flag.width * (9 / 16));
  }

  static getFlagPath(regionISO, size) {
    return `/images/flags/${regionISO}_icon_${size}.png`;
  }

  static getFlagUrl(regionISO, size) {
    return `https://www.privateinternetaccess.com/images/flags/icons/${regionISO}_icon_${size}px.png`;
  }

  static async generateIcon(imageData, size, region) {
    let flag = null;
    const images = imageData;
    const robot = await Icon.newImage(greenRobots[size]);
    const ctx = Icon.drawImage(Icon.newCanvasCtx(robot), robot);

    try {
      flag = await Icon.newImage(Icon.getFlagPath(region.iso, size));
    } catch (e) {
      try {
        flag = await Icon.newImage(Icon.getFlagUrl(region.iso, size));
      } catch (err) {
        debug(`icon.js: flag icon failed`);
      }
    }

    if (flag) {
      Icon.drawFlagOnto(ctx, flag);
    }

    images[size] = ctx.getImageData(0, 0, robot.width, robot.height);
  }

  static async generateErrorIcon(imageData, size) {
    const images = imageData;
    const redrobot = await Icon.newImage(redRobots[size]);
    const ctx = Icon.drawImage(Icon.newCanvasCtx(redrobot), redrobot);
    images[size] = ctx.getImageData(0, 0, redrobot.width, redrobot.height);
  }

}

/* harmony default export */ __webpack_exports__["a"] = (Icon);

/***/ }),
/* 118 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var _helpers_http__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(15);
/* harmony import */ var os__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(178);
/* harmony import */ var os__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(os__WEBPACK_IMPORTED_MODULE_1__);


/**
 * I18n is a wrapper around the browser translation service
 *
 * We first attempt to come up with the translations ourselves, and
 * if such a translation cannot be found we fallback to the
 * chrome.i18n API
 */

class I18n {
  constructor(app) {
    // bindings
    this.init = this.init.bind(this);
    this.t = this.t.bind(this);
    this.detectLocale = this.detectLocale.bind(this);
    this.detectBrowserLocale = this.detectBrowserLocale.bind(this);
    this.changeLocale = this.changeLocale.bind(this);
    this.getWorker = this.getWorker.bind(this);
    this.domain = this.domain.bind(this); // init

    window.t = this.t;
    this.app = app;
    this.rerouteMap = new Map([['pt', 'pt_BR']]);
    this.domainMap = I18n.createDomainMap();
    this.languageMap = I18n.createLanguageMap();
    this.worker = null;
    this.defaultLocale = 'en';
    this.acceptedLocales = Array.from(this.languageMap.keys());
    this.locale = this.detectLocale() || this.defaultLocale;
    this.translations = new Map([]);
    this.initializing = this.init();
  }

  async init() {
    try {
      await this.changeLocale(this.locale);
    } catch (_) {
      debug(`i18n: error setting locale "${this.locale}"`);

      if (this.locale !== this.defaultLocale) {
        try {
          await this.changeLocale(this.defaultLocale);
          debug(`i18n: fell back to default locale: ${this.defaultLocale}`);
        } catch (__) {
          debug(`i18n: fall back to default locale(${this.defaultLocale}) failed`);
        }
      }
    }
  }
  /**
   * Find the translation for a given key
   */


  t(key, variables = {}) {
    let message = this.translations.get(key) || chrome.i18n.getMessage(key);
    Object.keys(variables).forEach(varKey => {
      message = message.replace(new RegExp(`%{${varKey}}`, 'g'), variables[varKey]);
    });

    if (message.includes('%{browser}')) {
      message = message.replace(new RegExp('%{browser}', 'g'), this.app.buildinfo.browser);
    }

    if (message.includes('%{appVersion}')) {
      message = message.replace(new RegExp('%{appVersion}', 'g'), `v${this.app.buildinfo.version}`);
    }

    if (message.includes('%{region}')) {
      const region = this.app.util.regionlist.getSelectedRegion();
      message = message.replace(new RegExp('%{region}', 'g'), region.localizedName());
    }

    return message;
  }

  detectLocale() {
    const {
      storage
    } = this.app.util;
    const storageLocale = storage.getItem('locale');
    const locale = storageLocale || this.detectBrowserLocale();

    if (this.acceptedLocales.includes(locale)) {
      return locale;
    }

    return undefined;
  }

  detectBrowserLocale() {
    let locale = chrome.i18n.getUILanguage().replace(/-/g, '_');

    if (this.languageMap.has(locale)) {
      return locale;
    }

    locale = locale.slice(0, 2);
    return this.rerouteMap.get(locale) || locale;
  }

  changeLocale(locale) {
    const {
      icon
    } = this.app.util;

    if (!this.acceptedLocales.includes(locale)) {
      return Promise.reject();
    }

    let targetURL = chrome.extension.getURL(`/_locales/${locale}/messages.json`);
    this.worker = _helpers_http__WEBPACK_IMPORTED_MODULE_0__[/* default */ "a"].get(targetURL).then(async res => {
      const json = await res.json();
      this.translations.clear();
      Object.keys(json).forEach(key => {
        this.translations.set(key, json[key].message);
      });
      this.locale = locale;
      icon.updateTooltip();
      this.worker = null;
      return locale;
    }).catch(res => {
      this.worker = null;
      throw res;
    });
    return this.worker;
  }

  getWorker() {
    return this.worker;
  }

  domain() {
    return this.domainMap.get(this.locale) || this.domainMap.get('en');
  }

  static createLanguageMap() {
    return new Map([['en', 'English'], ['de', 'Deutsch'], ['fr', 'Français'], ['ru', 'Русский'], ['it', 'Italiano'], ['nl', 'Nederlands'], ['tr', 'Türkçe'], ['pl', 'Polski'], ['pt_BR', 'Português (Brasil)'], ['ja', '日本語'], ['es', 'Español (México)'], ['da', 'Dansk'], ['th', 'ไทย'], ['zh_TW', '繁體中文'], ['zh_CN', '简体中文'], ['ar', 'ةيبرعلا'], ['ko', '한국어']]);
  }

  static createDomainMap() {
    return new Map([['en', 'www.privateinternetaccess.com'], ['nl', 'nld.privateinternetaccess.com'], ['fr', 'fra.privateinternetaccess.com'], ['ru', 'rus.privateinternetaccess.com'], ['it', 'ita.privateinternetaccess.com'], ['ko', 'kor.privateinternetaccess.com'], ['no', 'nor.privateinternetaccess.com'], ['pl', 'pol.privateinternetaccess.com'], ['es', 'mex.privateinternetaccess.com'], ['ar', 'ara.privateinternetaccess.com'], ['th', 'tha.privateinternetaccess.com'], ['tr', 'tur.privateinternetaccess.com'], ['ja', 'jpn.privateinternetaccess.com'], ['da', 'dnk.privateinternetaccess.com'], ['de', 'deu.privateinternetaccess.com'], ['pt_BR', 'bra.privateinternetaccess.com'], ['zh_CN', 'chi.privateinternetaccess.com'], ['zh_TW', 'cht.privateinternetaccess.com']]);
  }

}

/* harmony default export */ __webpack_exports__["a"] = (I18n);

/***/ }),
/* 119 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return Logger; });
/* harmony import */ var _helpers_isDev__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(102);

/**
 * The logger collects useful information from the extension
 * for debugging purposes.
 *
 * IMPORTANT: only active when setting is enabled (disabled by default)
 * IMPORTANT: only development builds log to console (not qa, beta or release)
 */

class Logger {
  constructor(app) {
    this.app = app;
    this.entries = [];
    this.MAX_LOG_SIZE = 200; // bindings

    this.debug = this.debug.bind(this);
    this.getEntries = this.getEntries.bind(this);
  }

  debug(message, condition) {
    if (condition && !condition()) {
      return message;
    }

    if (Object(_helpers_isDev__WEBPACK_IMPORTED_MODULE_0__[/* default */ "a"])()) {
      // eslint-disable-next-line no-console
      console.log(message);
    }

    if (this.app.util.settings.getItem('debugmode')) {
      // remove extraneous entries
      while (this.entries.length >= this.MAX_LOG_SIZE) {
        this.entries.shift();
      } // add this error to the debug log


      this.entries.push([new Date().toISOString(), Logger.stringify(message)]); // update any UIs with new debug messages

      if (typeof browser == 'undefined') {
        this.app.courier.sendMessage('refresh');
      }
    }

    return message;
  }

  getEntries() {
    return Array.from(this.entries).reverse();
  }

  removeEntries() {
    this.entries = [];

    if (typeof browser == 'undefined') {
      this.app.courier.sendMessage('refresh');
    }
  }

  static stringify(message) {
    if (typeof message === 'string') {
      return message;
    }

    return JSON.stringify(message);
  }

}

/***/ }),
/* 120 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
class Storage {
  constructor(app) {
    // Bindings
    this.hasItem = this.hasItem.bind(this);
    this.getItem = this.getItem.bind(this);
    this.setItem = this.setItem.bind(this);
    this.removeItem = this.removeItem.bind(this); // Init

    this.app = app;
    this.stores = {
      [Storage.MEMORY]: window.sessionStorage,
      [Storage.LOCAL]: window.localStorage
    };
  }
  /* ------------------------------------ */

  /*               Public                 */

  /* ------------------------------------ */


  hasItem(key, store = Storage.LOCAL) {
    if (Storage.validateStoreAndKey({
      store,
      key
    })) {
      const item = this.getItem(key, store);
      return item !== null;
    }

    throw Storage.createOperationError('has');
  }

  getItem(key, store = Storage.LOCAL) {
    if (Storage.validateStoreAndKey({
      store,
      key
    })) {
      return this.stores[store].getItem(key);
    }

    throw Storage.createOperationError('get');
  }

  setItem(key, value, store = Storage.LOCAL) {
    if (Storage.validateStoreAndKey({
      store,
      key
    })) {
      let storageValue;

      if (typeof value === 'undefined' || value === null) {
        storageValue = '';
      } else {
        storageValue = value;
      }

      this.stores[store].setItem(key, storageValue);
    } else {
      throw Storage.createOperationError('set');
    }
  }

  removeItem(key, store = Storage.LOCAL) {
    if (Storage.validateStoreAndKey({
      store,
      key
    })) {
      this.stores[store].removeItem(key);
    } else {
      throw Storage.createOperationError('remove');
    }
  }
  /* ------------------------------------ */

  /*               Static                 */

  /* ------------------------------------ */


  static validateStore(store) {
    switch (store) {
      case Storage.LOCAL:
      case Storage.MEMORY:
        return true;

      default:
        debug(`no such storage type: ${store}`);
        return false;
    }
  }

  static validateKey(key) {
    const type = typeof key;
    const isString = type === 'string';
    const isEmpty = isString && !key;

    if (!isString || isEmpty) {
      let msg = 'key must be a valid string. ';

      if (!isString) {
        msg += `was: ${type}`;
      } else {
        msg += 'was: empty string';
      }

      console.debug(msg);
      return false;
    }

    return true;
  }

  static validateStoreAndKey({
    store,
    key
  }) {
    return Storage.validateStore(store) && Storage.validateKey(key);
  }

  static createOperationError(operation) {
    // Refer to errors thrown in validateStore or validateKey
    return new Error(`could not ${operation} item, see above error for more information`);
  }

}

Storage.LOCAL = 'localStorage';
Storage.MEMORY = 'memoryStorage';
/* harmony default export */ __webpack_exports__["a"] = (Storage);

/***/ }),
/* 121 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
class Counter {
  constructor(app) {
    // bindings
    this.get = this.get.bind(this);
    this.inc = this.inc.bind(this);
    this.del = this.del.bind(this); // init

    this.app = app;
    this.table = {};
  }

  get(member) {
    return this.table[member] || 0;
  }

  inc(member) {
    this.table[member] = (this.table[member] || 0) + 1;
  }

  del(member) {
    delete this.table[member];
  }

}

/* harmony default export */ __webpack_exports__["a"] = (Counter);

/***/ }),
/* 122 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var _helpers_reportError__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(64);

/* Types

  interface AppSetting {
    settingDefault: boolean;
    settingID: string;
  }

  interface ContentSetting extends AppSetting {
    clearSetting(): void;
    applySetting(): void;
    isApplied(): boolean;
  }

  interface ChromeSetting extends ApiSetting {
    isApplied(): boolean;
    isControllable(): boolean;
  }

  type ApiSetting = ContentSetting | ChromeSetting;
*/

const ApplicationIDs = {
  BLOCK_PLUGINS: 'blockplugins',
  BLOCK_UTM: 'blockutm',
  BLOCK_FBCLID: 'blockfbclid',
  MACE_PROTECTION: 'maceprotection',
  DEBUG_MODE: 'debugmode',
  REMEMBER_ME: 'rememberme',
  FIRST_RUN: 'firstRun',
  DARK_THEME: 'darkTheme',
  HTTPS_UPGRADE: 'httpsUpgrade',
  ALWAYS_ON: 'alwaysActive'
};
/**
 * Keep track of the status of various settings
 * in the extension
 */

class Settings {
  constructor(app) {
    // properties
    this.app = app;
    this.appDefaults = Settings.appDefaults; // bindings

    this.init = this.init.bind(this);
    this.hasItem = this.hasItem.bind(this);
    this.getItem = this.getItem.bind(this);
    this.setItem = this.setItem.bind(this);
    this.toggle = this.toggle.bind(this);
    this.getAll = this.getAll.bind(this);
    this.getControllable = this.getControllable.bind(this);
    this.enabled = this.enabled.bind(this);
  }
  /* App Getters */


  get contentSettings() {
    const contentSettings = this.app.contentsettings ? this.app.contentsettings : {};
    return contentSettings;
  }

  get storage() {
    return this.app.util.storage;
  }

  get proxy() {
    return this.app.proxy;
  }

  get logger() {
    return this.app.logger;
  } // get contentSettings() { return this.app.contentsettings; }


  get chromeSettings() {
    return this.app.chromesettings;
  }

  get regionlist() {
    return this.app.util.regionlist;
  }

  get adapter() {
    return this.app.adapter;
  }
  /* Transformations */


  get apiSettings() {
    return [...Object.values(this.contentSettings), ...Object.values(this.chromeSettings)];
  }

  get allSettings() {
    return [...this.appDefaults, ...this.apiSettings];
  }

  get appIDs() {
    return this.appDefaults.map(setting => {
      return setting.settingID;
    });
  }

  get apiIDs() {
    return this.apiSettings.map(setting => {
      return setting.settingID;
    });
  }

  get settingIDs() {
    return this.allSettings.map(setting => {
      return setting.settingID;
    });
  }

  getInternalApiSetting(settingID) {
    return this.apiSettings.find(setting => {
      return setting.settingID === settingID;
    });
  }

  existsApplicationSetting(settingID) {
    return Boolean(this.appDefaults.find(setting => {
      return setting.settingID === settingID;
    }));
  }

  validID(settingID) {
    if (!this.settingIDs.includes(settingID)) {
      debug(`invalid settingID: ${settingID}`);
      return false;
    }

    return true;
  }

  toggleSetting(settingID) {
    const newValue = !this.getItem(settingID);
    this.setItem(settingID, newValue);
    return newValue;
  }
  /**
   * Toggle application setting (side effects handled here)
   *
   * @param {string} settingID id of setting
   *
   * @returns {boolean} new value of setting
   */


  toggleApplicationSetting(settingID) {
    const newValue = this.toggleSetting(settingID);

    switch (settingID) {
      case ApplicationIDs.MACE_PROTECTION:
        if (this.app.proxy.enabled()) {
          this.app.proxy.enable().catch(Object(_helpers_reportError__WEBPACK_IMPORTED_MODULE_0__[/* default */ "a"])('settings.js'));
        }

        break;

      case ApplicationIDs.DEBUG_MODE:
        if (!newValue) {
          this.logger.removeEntries();
        }

        break;

      default:
        break;
    }

    return newValue;
  }
  /**
   * Toggle API Setting (side effects handled by setting)
   *
   * @param {ApiSetting} setting Api Setting to toggle
   *
   * @returns {Promise<boolean>} new value of setting;
   */


  async toggleApiSetting(setting) {
    const toggle = setting.isApplied() ? setting.clearSetting : setting.applySetting;

    try {
      await toggle.call(setting);
    } catch (_) {
      debug(`failed to toggle setting: ${setting.settingID}`);
    }

    const newValue = setting.isApplied();
    this.setItem(setting.settingID, newValue);
    return newValue;
  }

  enabled() {
    const {
      app: {
        util: {
          user
        }
      }
    } = this;
    return user.getLoggedIn();
  }
  /**
   * Initialize the setting values
   *
   * @returns {void}
   */


  init() {
    this.allSettings.forEach(setting => {
      if (!this.hasItem(setting.settingID)) {
        this.setItem(setting.settingID, setting.settingDefault, true);
      }
    });
  }
  /**
   * Toggle the specified setting
   *
   * @param {string} settingID ID for setting
   *
   * @returns {Promise<boolean>} New value of setting
   *
   * @throws {Error} if settingID is not valid
   */


  async toggle(settingID, bridged) {
    if (!bridged && typeof browser != 'undefined') {
      this.adapter.sendMessage('util.settings.toggle', {
        settingID
      });
    } // Look for setting in application settings


    if (this.existsApplicationSetting(settingID)) {
      return this.toggleApplicationSetting(settingID);
    }

    const apiSetting = this.getInternalApiSetting(settingID);

    if (apiSetting) {
      return this.toggleApiSetting(apiSetting);
    } // No such setting


    throw new Error(`settings.js: no such setting: ${settingID}`);
  }
  /**
   * Determine whether the setting exists yet
   *
   * @param {string} settingID ID for setting
   *
   * @returns {boolean} whether setting exists in storage
   *
   * @throws {Error} if settingID is not valid
   */


  hasItem(settingID) {
    if (this.validID(settingID)) {
      return this.storage.hasItem(`settings:${settingID}`);
    }

    throw new Error('settings.js: cannot perform hasItem without valid settingID');
  }
  /**
   * Get the specified setting value
   *
   * @param {string} settingID ID for setting
   *
   * @returns {boolean} value of setting
   *
   * @throws {Error} if settingID is not valid
   */


  getItem(settingID, defaultValue = null) {
    if (this.validID(settingID)) {
      const value = this.storage.getItem(`settings:${settingID}`);

      if (value === null) {
        return defaultValue;
      }

      return typeof browser == 'undefined' ? !!this.storage.getItem(`settings:${settingID}`) : value === String(true);
    }

    throw new Error('settings.js: cannot perform get without valid settingID');
  }
  /**
   * Check if specified setting is active
   *
   * @param {string} settingID
   */


  isActive(settingID) {
    if (this.validID(settingID)) {
      const loggedIn = this.app.util.user.getLoggedIn();

      if (!loggedIn) {
        return false;
      }

      const value = this.getItem(settingID);

      if (!value) {
        return false;
      }

      const alwaysActive = this.getItem('alwaysActive');

      if (alwaysActive) {
        return value;
      }

      const proxyValue = this.app.proxy.getEnabled();
      return proxyValue && value;
    }

    throw new Error('settings.js: cannot perform isActive without valid settingID');
  }
  /**
   * Set the value of specified setting
   *
   * @param {string} settingID ID of setting
   * @param {boolean} value new value for setting
   *  
   * @throws {Error} if settingID is not valid
   *
   * @returns {void}
   */


  setItem(settingID, value, bridged) {
    if (this.validID(settingID)) {
      const newValue = String(value) === 'true';
      const key = `settings:${settingID}`;
      this.storage.setItem(key, newValue);

      if (!bridged && typeof browser != 'undefined') {
        this.adapter.sendMessage('updateSettings', {
          settingID,
          value: newValue
        });
      }
    } else {
      throw new Error('cannot perform setItem with invalid settingID');
    }
  }

  getAll() {
    return this.settingIDs.map(settingID => {
      return {
        settingID,
        value: this.getItem(settingID)
      };
    });
  }

  getAvailable(settingID) {
    if (this.validID(settingID)) {
      if (Object.values(ApplicationIDs).includes(settingID)) {
        return true;
      }

      if (this.apiIDs.includes(settingID)) {
        const setting = this.getApiSetting(settingID);

        if (typeof setting.isAvailable === 'function') {
          return setting.isAvailable();
        }

        return true;
      }

      return true;
    }

    throw new Error('settings.js: cannot get available w/o valid settingID');
  }
  /**
   * Determine whether specified setting is controllable by user
   *
   * @param {string} settingID ID for setting
   *
   * @returns {boolean} Whether the setting is controllable by user
   *
   * @throws {Error} if settingID is not valid
   */


  getControllable(settingID) {
    if (this.validID(settingID)) {
      if (this.apiIDs.includes(settingID)) {
        const setting = this.getInternalApiSetting(settingID); // Chromesettings have function

        if (typeof setting.isControllable === 'function') {
          return setting.isControllable();
        }

        return true;
      } // By default controllable is true


      return true;
    }

    throw new Error('settings.js: cannot get controllable without valid settingID');
  }
  /**
   * Get the actual setting for specified API settingID
   *
   * @param {string} settingID ID of setting
   *
   * @returns {ApiSetting} setting corresponding to settingID
   *
   * @throws {Error} if settingID is not valid API setting
   */


  getApiSetting(settingID) {
    if (!this.validID(settingID)) {
      throw new Error('invalid settingID');
    } else if (this.apiIDs.includes(settingID)) {
      return this.apiSettings.find(s => {
        return s.settingID === settingID;
      });
    } else {
      throw new Error('settings.js: getApiSetting requires settingID for ApiSetting, not AppSetting');
    }
  }
  /**
   * Default values for Application Settings
   *
   * Also used as list of acceptable application settingID's
   */


  static get appDefaults() {
    return [{
      settingID: ApplicationIDs.BLOCK_PLUGINS,
      settingDefault: true
      /* TODO: unused until a bug in chrome is fixed. */

    }, {
      settingID: ApplicationIDs.BLOCK_UTM,
      settingDefault: false
    }, {
      settingID: ApplicationIDs.BLOCK_FBCLID,
      settingDefault: false
    }, {
      settingID: ApplicationIDs.MACE_PROTECTION,
      settingDefault: false
    }, {
      settingID: ApplicationIDs.DEBUG_MODE,
      settingDefault: false
    }, {
      settingID: ApplicationIDs.REMEMBER_ME,
      settingDefault: true
    }, {
      settingID: ApplicationIDs.FIRST_RUN,
      settingDefault: true
    }, {
      settingID: ApplicationIDs.DARK_THEME,
      settingDefault: true
    }, {
      settingID: ApplicationIDs.HTTPS_UPGRADE,
      settingDefault: false
    }, {
      settingID: ApplicationIDs.ALWAYS_ON,
      settingDefault: true
    }];
  }

}

/* harmony default export */ __webpack_exports__["a"] = (Settings);

/***/ }),
/* 123 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
class ErrorInfo {
  constructor(app) {
    // bindings
    this.set = this.set.bind(this);
    this.get = this.get.bind(this);
    this.delete = this.delete.bind(this); // init

    this.app = app;
    this.errorMap = new Map();
  }

  set(errorName, url) {
    const errorID = ErrorInfo.generateID();
    this.errorMap.set(errorID, [errorName, url]);
    return errorID;
  }

  get(errorID) {
    return this.errorMap.get(errorID) || [];
  }

  delete(errorID) {
    const deleted = this.errorMap.delete(errorID);

    if (deleted) {
      debug(`errorinfo.js: delete ${errorID}`);
    } else {
      debug(`errorinfo.js: miss ${errorID}`);
    }

    return deleted;
  }

  static generateID() {
    let errorID = '';

    for (let i = 0; i < 3; i++) {
      errorID += Math.random().toString(36);
    }

    return errorID;
  }

}

/* harmony default export */ __webpack_exports__["a"] = (ErrorInfo);

/***/ }),
/* 124 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* WEBPACK VAR INJECTION */(function(process) {class BuildInfo {
  constructor() {
    this.name = "public";
    this.version = "3.2.0";
    this.date = new Date("Mon, 28 Feb 2022 14:59:16 GMT");
    this.debug = "production" !== 'production';
    this.coupon = "PIACHROME";
    this.gitcommit = process.env.COMMIT_HASH;
    this.gitbranch = process.env.GIT_BRANCH;
    this.browser = BuildInfo.getFormattedBrowser();
  }

  static getFormattedBrowser() {
    const browser = "chrome";
    const [firstChar] = browser;
    const tail = browser.slice(1);
    return firstChar.toLocaleUpperCase() + tail;
  }

}

/* harmony default export */ __webpack_exports__["a"] = (BuildInfo);
/* WEBPACK VAR INJECTION */}.call(this, __webpack_require__(179)))

/***/ }),
/* 125 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var _helpers_http__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(15);
/* harmony import */ var _helpers_messagingFirefox__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(4);



const defaultRegions = __webpack_require__(180);

const FAVORITE_REGIONS_KEY = "favoriteregions";
const OVERRIDE_KEY = "regionlist::override";

class RegionList {
  constructor(app, foreground) {
    // bindings
    this.testHost = this.testHost.bind(this);
    this.testPort = this.testPort.bind(this);
    this.getPotentialRegions = this.getPotentialRegions.bind(this);
    this.getPort = this.getPort.bind(this);
    this.getPotentialHosts = this.getPotentialHosts.bind(this);
    this.getPotentialPorts = this.getPotentialPorts.bind(this);
    this.initialOverrideRegions = this.initialOverrideRegions.bind(this);
    this.addOverrideRegion = this.addOverrideRegion.bind(this);
    this.updateOverrideRegion = this.updateOverrideRegion.bind(this);
    this.removeOverrideRegion = this.removeOverrideRegion.bind(this);
    this.getOverrideArray = this.getOverrideArray.bind(this);
    this.updateRegion = this.updateRegion.bind(this);
    this.export = this.export.bind(this);
    this.import = this.import.bind(this);
    this.getRegion = this.getRegion.bind(this);
    this.hasRegions = this.hasRegions.bind(this);
    this.hasRegion = this.hasRegion.bind(this);
    this.getIsAuto = this.getIsAuto.bind(this);
    this.setIsAuto = this.setIsAuto.bind(this);
    this.getFastestRegion = this.getFastestRegion.bind(this);
    this.getAutoRegion = this.getAutoRegion.bind(this);
    this.setAutoRegion = this.setAutoRegion.bind(this);
    this.getRegions = this.getRegions.bind(this);
    this.toArray = this.toArray.bind(this);
    this.isSelectedRegion = this.isSelectedRegion.bind(this);
    this.getSelectedRegion = this.getSelectedRegion.bind(this);
    this.getRegionFromStorage = this.getRegionFromStorage.bind(this);
    this.importAutoRegion = this.importAutoRegion.bind(this);
    this.setSelectedRegion = this.setSelectedRegion.bind(this);
    this.sync = this.sync.bind(this);
    this.setFavoriteRegion = this.setFavoriteRegion.bind(this);
    this.setDefaultRegions = this.setDefaultRegions.bind(this);
    this.getRegionById = this.getRegionById.bind(this);
    this.exportAutoRegion = this.exportAutoRegion.bind(this); // init

    this.app = app;
    this.foreground = foreground;
    this.selectedRegionSmartLoc = null;
    this.storage = this.app.util.storage;
    this.normalRegions = {};
    this.overrideRegions = this.initialOverrideRegions(this.storage);
    this.defaultRegions = defaultRegions; // set isAuto property based on storage

    const isAuto = !!this.app.util.storage.getItem("autoRegion");
    const region = this.app.util.storage.getItem("region");

    if (isAuto === "true") {
      this.isAuto = true;
    } else if (!isAuto && !region) {
      this.isAuto = true;
    } else {
      this.isAuto = false;
    } // poll for new regions every 60 minutes


    this.setDefaultRegions();
    chrome.alarms.create("PollRegionList", {
      delayInMinutes: 30,
      periodInMinutes: 60
    });
  }

  setDefaultRegions() {
    const {
      util: {
        storage
      }
    } = this.app; // keep track of current favorite regions

    let favoriteRegions = storage.getItem("favoriteregions");

    if (favoriteRegions) {
      favoriteRegions = favoriteRegions.split(",");
    } else {
      favoriteRegions = [];
    } // clear current region data


    this.normalRegions = {}; // replace with new data from server

    defaultRegions.map(reg => {
      const region = RegionList.createNormalRegion(reg.name, reg);

      if (favoriteRegions.includes(region.id)) {
        region.isFavorite = true;
      }

      this.normalRegions[region.id] = region;
    });
  } // ---------------------- Auth Tests --------------------- //

  /**
   * Test to see if the provided host is potentially used w/ active proxy
   *
   * @param {string} host The host to test
   */


  testHost(host) {
    return this.getPotentialHosts().includes(host);
  }
  /**
   * Test to see if the provided port is potentially used w/ active proxy
   *
   * @param {number} port The port to test
   */


  testPort(port) {
    return this.getPotentialPorts().includes(port);
  }

  getPotentialRegions() {
    let regions;
    const {
      util: {
        storage
      }
    } = this.app;
    const fromStorage = storage.getItem("region");
    const fromMemory = this.getRegions();

    if (fromStorage) {
      const storageRegion = JSON.parse(fromStorage);
      regions = Object.assign({}, fromMemory, {
        [storageRegion.id]: storageRegion
      });
    } else {
      regions = fromMemory;
    }

    return Object.values(regions);
  } // ------------------------ Firefox ------------------------- //
  // ---------------------------------------------------------- //
  //    The following methods are used by the mockApp system    //
  // ---------------------------------------------------------- //


  importAutoRegion(autoRegion) {
    if (!autoRegion) {
      return;
    }

    this.setAutoRegion(RegionList.createNormalRegion(autoRegion.id, autoRegion), true);
  }

  import(regions) {
    if (!regions || !Array.isArray(regions)) {
      return;
    }

    regions.forEach(region => {
      this.updateRegion(RegionList.localize(region));
    });
    this.app.util.bypasslist.updatePingGateways();
  }

  export() {
    // Important to use ALL regions (override regions will override normal regions in toArray)
    return [...Object.values(this.overrideRegions), ...Object.values(this.normalRegions)].map(region => {
      // strip non-serializable properties
      return JSON.parse(JSON.stringify(region));
    });
  }

  exportAutoRegion() {
    if (!this.autoRegion) {
      return undefined;
    }

    return {
      id: this.autoRegion.id,
      ping: this.autoRegion.ping,
      name: this.autoRegion.name,
      iso: this.autoRegion.iso,
      dns: this.autoRegion.host,
      port: this.autoRegion.port,
      macePort: this.autoRegion.macePort,
      latency: this.autoRegion.latency
    };
  }

  resetFavoriteRegions(regions) {
    const {
      util: {
        storage
      }
    } = this.app;
    storage.setItem(FAVORITE_REGIONS_KEY, regions);

    if (regions) {
      regions.split(",").forEach(region => {
        const memRegion = this.getRegion(region.id);

        if (memRegion) {
          this.updateRegion(Object.assign({}, memRegion, {
            isFavorite: !memRegion.isFavorite
          }));
        }
      });
    }
  } // -------------------- Static ----------------------- //

  /**
   * Get a list of hosts that are potentially being used for the active proxy connection
   */


  getPotentialHosts() {
    return this.getPotentialRegions().map(r => {
      return r.host;
    });
  }
  /**
   * Get a list of ports that are potentially being used for the active proxy connection
   */


  getPotentialPorts() {
    const {
      util: {
        settings
      }
    } = this.app;
    const key = settings.getItem("maceprotection") ? "macePort" : "port";
    return this.getPotentialRegions().map(r => {
      return r[key];
    });
  } // -------------------- Override Regions ----------------------- //


  initialOverrideRegions() {
    let overrideRegions;
    const fromStorage = this.storage.getItem(OVERRIDE_KEY);

    if (fromStorage) {
      overrideRegions = {};
      const fromStorageMap = typeof fromStorage == "string" ? JSON.parse(fromStorage) : fromStorage;
      Object.keys(fromStorageMap).forEach(id => {
        overrideRegions[id] = RegionList.localize(fromStorageMap[id]);
      });
    } else {
      overrideRegions = {};
      this.storage.setItem(OVERRIDE_KEY, JSON.stringify(overrideRegions));
    }

    return overrideRegions;
  }
  /**
   * Add a new override region
   */


  addOverrideRegion({
    name,
    host,
    port
  }, stopPropagation) {
    const {
      app: {
        adapter
      }
    } = this;

    try {
      const region = RegionList.createOverrideRegion({
        name,
        host,
        port
      });
      this.updateOverrideRegion(region);

      if (!stopPropagation && typeof browser != "undefined") {
        adapter.sendMessage(_helpers_messagingFirefox__WEBPACK_IMPORTED_MODULE_1__["Type"].ADD_OVERRIDE_REGION, {
          name,
          host,
          port
        });
      }
    } catch (err) {
      const msg = err.message || err;
      debug(msg);
      throw err;
    }
  }

  updateOverrideRegion(region) {
    if (!region.override || !region.id) {
      throw new Error("invalid region");
    }

    this.overrideRegions[region.id] = region;
    this.storage.setItem(OVERRIDE_KEY, JSON.stringify(this.overrideRegions));
  }
  /**
   * Remove an existing override region by name
   */


  removeOverrideRegion(name, stopPropagation) {
    const {
      app: {
        adapter
      }
    } = this;
    let wasSelected = false;
    const id = RegionList.createOverrideID(name);
    const region = this.overrideRegions[id];
    delete this.overrideRegions[id];

    if (region && region.active) {
      wasSelected = true;
      let toSelect = this.getFastestRegion();

      if (!toSelect) {
        [toSelect] = this.getRegions();
      }

      if (toSelect) {
        this.setSelectedRegion(this.getFastestRegion().id);
      }
    }

    this.storage.setItem(OVERRIDE_KEY, JSON.stringify(this.overrideRegions));

    if (!stopPropagation && typeof browser != "undefined") {
      adapter.sendMessage(_helpers_messagingFirefox__WEBPACK_IMPORTED_MODULE_1__["Type"].REMOVE_OVERRIDE_REGION, name);
    }

    return wasSelected;
  }
  /**
   * Retrieve an array of override regions
   */


  getOverrideArray() {
    return Object.values(this.overrideRegions);
  } // --------------------- General ---------------------- //


  updateRegion(region) {
    if (region.override) {
      this.updateOverrideRegion(region);
    } else {
      this.normalRegions[region.id] = region;
    }
  }

  getRegion(id) {
    return this.getRegions()[id];
  }

  getPort() {
    const {
      util: {
        settings
      }
    } = app;
    const key = settings.getItem("maceprotection") ? "macePort" : "port";
    return key;
  }
  /**
   * Returns whether there are regions in memory
   */


  hasRegions() {
    return !!this.toArray().length;
  }

  hasRegion(id) {
    return !!this.getRegion(id);
  }
  /**
   * Returns the isAuto flag, this determines whether the extension is in 'auto' mode
   */


  getIsAuto() {
    return this.isAuto;
  }
  /**
   * Sets the given value to isAuto and saves that value to storage
   */


  setIsAuto(value) {
    this.isAuto = value;
    this.app.util.storage.setItem("autoRegion", value);
  }
  /**
   * Calculates the fastest region given current latency times.
   * Can return undefined if no regions exists.
   */


  getFastestRegion() {
    if (!this.hasRegions()) {
      return undefined;
    }

    const regions = this.toArray();
    const {
      regionsorter
    } = this.app.util;
    const sorted = regionsorter.latencySort(regions);
    return sorted[0];
  }
  /**
   * Returns the 'auto' region, the fastest region based on latency
   */


  getAutoRegion() {
    this.setAutoRegion(this.getFastestRegion());
    return this.autoRegion;
  }
  /**
   * Sets autoRegion to an immutable copy of given region value.
   */


  setAutoRegion(region, stopPropagation) {
    this.autoRegion = Object.assign({}, region);
    const {
      adapter
    } = this.app;

    if (!stopPropagation && typeof browser != "undefined") {
      adapter.sendMessage(_helpers_messagingFirefox__WEBPACK_IMPORTED_MODULE_1__["Type"].IMPORT_AUTO_REGION, this.exportAutoRegion());
    }
  }

  getRegions() {
    return Object.assign({}, this.normalRegions, this.overrideRegions);
  }
  /**
   * Iterates through the regionMap and sets the active property to false for all regions.
   */


  clearActive() {
    this.toArray().forEach(currentRegion => {
      const thisRegion = currentRegion;
      thisRegion.active = false;
    });
  }

  toArray() {
    return Object.values(this.getRegions());
  }

  isSelectedRegion(region) {
    if (!this.getSelectedRegion()) {
      return false;
    }

    return this.getSelectedRegion().id === region.id;
  }
  /*
    NOTE: we keep an on-disk copy of the last selected region,
    incase this method is called when the region list has
    not synced.
  */


  getRegionById(id) {
    if (id) {
      return Object.values(this.getRegions()).filter(v => v.id === id)[0];
    }
  }

  getSelectedRegion() {
    let selectedRegion;
    let storageRegion; // check if auto region is used

    if (this.getIsAuto()) {
      selectedRegion = this.getAutoRegion();
    } // look for active region in memory


    if (!selectedRegion) {
      selectedRegion = this.toArray().find(region => {
        return region.active;
      });
    } // look for active region in storage


    if (!selectedRegion) {
      storageRegion = this.storage.getItem("region");
    }

    if (!selectedRegion && storageRegion) {
      try {
        selectedRegion = RegionList.localize(JSON.parse(storageRegion));
      } catch (_) {
        /* noop */
      }
    }

    const region = this.selectedRegionSmartLoc ? Object.values(this.getRegions()).filter(v => v.id === this.selectedRegionSmartLoc.id) : [];
    selectedRegion = region.length > 0 ? region[0] : selectedRegion; // selectedRegion can be undefined if there are no regions

    return selectedRegion;
  }

  getRegionFromStorage() {
    let selectedRegion;
    let storageRegion; // check if auto region is used

    if (this.getIsAuto()) {
      selectedRegion = this.getAutoRegion();
    } // look for active region in memory


    if (!selectedRegion) {
      selectedRegion = this.toArray().find(region => {
        return region.active;
      });
    } // look for active region in storage


    if (!selectedRegion) {
      storageRegion = this.storage.getItem("region");
    }

    if (!selectedRegion && storageRegion) {
      try {
        selectedRegion = RegionList.localize(storageRegion);
      } catch (_) {
        /* noop */
      }
    }

    return selectedRegion;
  }

  setSelectedRegion(id, stopPropagation) {
    let selectedRegion;

    const clearRegion = r => {
      this.updateRegion(Object.assign({}, r, {
        active: false
      }));
    };

    const activeRegions = this.toArray().filter(r => {
      return r.active;
    });
    activeRegions.forEach(clearRegion);

    if (id === "auto") {
      this.setIsAuto(true);
      selectedRegion = this.getAutoRegion();
    } else {
      this.setIsAuto(false);
      selectedRegion = this.getRegion(id);

      if (!selectedRegion) {
        throw new Error(`no such region with id ${id}`);
      } // Set new region active


      this.updateRegion(Object.assign({}, selectedRegion, {
        active: true
      }));
    }

    this.storage.setItem("region", JSON.stringify(selectedRegion));

    if (!stopPropagation && typeof browser != "undefined") {
      this.app.adapter.sendMessage(_helpers_messagingFirefox__WEBPACK_IMPORTED_MODULE_1__["Type"].SET_SELECTED_REGION, {
        id
      });
    }
  }

  async sync() {
    const {
      courier,
      util: {
        storage,
        bypasslist,
        latencymanager
      }
    } = this.app; // keep track of current favorite regions

    let favoriteRegions = storage.getItem("favoriteregions");

    if (favoriteRegions) {
      favoriteRegions = favoriteRegions.split(",");
    } else {
      favoriteRegions = [];
    }

    RegionList.debug("start sync");

    try {
      // get latest regions from server
      const url = "https://serverlist.piaservers.net/proxy";
      const response = await _helpers_http__WEBPACK_IMPORTED_MODULE_0__[/* default */ "a"].get(url, {
        timeout: 5000
      });
      const json = await response.json(); // clear current region data

      this.normalRegions = {}; // replace with new data from server

      json.map(reg => {
        const region = RegionList.createNormalRegion(reg.name, reg);

        if (favoriteRegions.includes(region.id)) {
          region.isFavorite = true;
        }

        this.normalRegions[region.id] = region;
      }); // update bypasslist with new dns records

      bypasslist.updatePingGateways(); // update region latency

      await latencymanager.run(); // set new auto region

      this.setAutoRegion(this.getFastestRegion()); // if auto mode and proxy is on, just connect to the new auto region

      if (this.getIsAuto() && this.app.proxy.enabled()) {
        await this.app.proxy.enable();
      }

      courier.sendMessage("refresh");
      RegionList.debug("sync ok");
      return response;
    } catch (err) {
      RegionList.debug("sync error", err);
      return err;
    }
  }
  /**
   * Toggle whether or not the provided region is favorited
   *
   * @param {*|string} region Provided region to toggle
   */


  setFavoriteRegion(region, bridged) {
    const {
      util: {
        storage
      },
      adapter
    } = this.app; // Get regionID

    let regionID = "";

    if (typeof region === "string") {
      regionID = region;
    } else {
      regionID = region.id;
    } // alert background page if not bridged


    if (!bridged && typeof browser != "undefined") {
      adapter.sendMessage(_helpers_messagingFirefox__WEBPACK_IMPORTED_MODULE_1__["Type"].SET_FAVORITE_REGION, regionID);
    } // Determine current value of isFavorite


    let isFavorite = false;
    const memRegion = this.toArray().find(r => {
      return r.id === regionID;
    });
    ({
      isFavorite
    } = memRegion); // get current favorite regions from storage

    let currentFavs = storage.getItem("favoriteregions");

    if (currentFavs) {
      currentFavs = currentFavs.split(",");
    } else {
      currentFavs = [];
    } // update favorite regions in storage


    if (!isFavorite) {
      currentFavs.push(regionID);
      const favs = [...new Set(currentFavs)];
      storage.setItem("favoriteregions", favs.join(","));
    } else {
      currentFavs = currentFavs.filter(fav => {
        return fav !== regionID;
      });
      storage.setItem("favoriteregions", currentFavs.join(","));
    } // Update in memory region


    const newRegion = Object.assign({}, memRegion, {
      isFavorite: !isFavorite
    });
    this.updateRegion(newRegion);
  } // --------------------- Static ---------------------- //


  static createOverrideID(name) {
    return `override::${name.trim().toLowerCase()}`.replace(" ", "_");
  }

  static localize(region) {
    const localized = Object.assign({}, region, {
      localizedName() {
        if (localized.id.includes("override::")) {
          return localized.name;
        }

        const name = t(localized.id);
        return name.length > 0 ? name : localized.name;
      }

    });
    return localized;
  }

  static createOverrideRegion({
    name,
    host,
    port
  }) {
    if (!name) {
      throw new Error("name must not be empty");
    }

    if (!host) {
      throw new Error("host must not be empty");
    }

    if (typeof port !== "number") {
      throw new Error("port must be a number");
    }

    if (port < 0 || port > 65535) {
      throw new Error("invalid port range");
    }

    const lowerCaseName = name.toLowerCase();
    return RegionList.localize({
      id: RegionList.createOverrideID(lowerCaseName),
      override: true,
      name: lowerCaseName,
      host,
      ping: host,
      port,
      macePort: port,
      iso: "OR",
      scheme: "https",
      active: false,
      latency: "PENDING",
      offline: false,
      isFavorite: true,
      flag: "images/flags/override_icon_64.png"
    });
  }

  static createNormalRegion(regionID, region) {
    regionID = regionID.split(' ').join('_');
    return RegionList.localize({
      scheme: "https",
      id: regionID,
      ping: region.ping,
      name: region.name,
      iso: region.iso,
      host: region.dns,
      port: region.port,
      macePort: region.mace,
      flag: `/images/flags/${region.iso}_icon_64.png`,
      active: false,
      latency: "PENDING",
      offline: false,
      isFavorite: false,
      override: false
    });
  }

  static debug(msg, err) {
    const debugMsg = `regionlist.js: ${msg}`;
    debug(debugMsg);

    if (err) {
      const errMsg = `regionlist.js error: ${JSON.stringify(err, Object.getOwnPropertyNames(err))}`;
      debug(errMsg);
    }

    return new Error(debugMsg);
  }

}

/* harmony default export */ __webpack_exports__["a"] = (RegionList);

/***/ }),
/* 126 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return BypassList; });
/* harmony import */ var _helpers_messagingFirefox__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(4);

class BypassList {
  constructor(app, foreground) {
    // Bindings
    this.init = this.init.bind(this);
    this.generatePingGateways = this.generatePingGateways.bind(this);
    this.updatePingGateways = this.updatePingGateways.bind(this);
    this.isRuleEnabled = this.isRuleEnabled.bind(this);
    this.popularRulesByName = this.popularRulesByName.bind(this);
    this.visibleSize = this.visibleSize.bind(this);
    this.restartProxy = this.restartProxy.bind(this);
    this.getUserRules = this.getUserRules.bind(this);
    this.setUserRules = this.setUserRules.bind(this);
    this.addUserRule = this.addUserRule.bind(this);
    this.removeUserRule = this.removeUserRule.bind(this);
    this.enablePopularRule = this.enablePopularRule.bind(this);
    this.disablePopularRule = this.disablePopularRule.bind(this);
    this.enabledPopularRules = this.enabledPopularRules.bind(this);
    this.toArray = this.toArray.bind(this);
    this.saveRulesToFile = this.saveRulesToFile.bind(this);
    this.resetPopularRules = this.resetPopularRules.bind(this);
    this.importRules = this.importRules.bind(this);
    this.spawnImportTab = this.spawnImportTab.bind(this);
    this.getRulesSmartLoc = this.getRulesSmartLoc.bind(this); // Init

    this.app = app;
    this.foreground = foreground;
    this.storage = app.util.storage;
    this.storageKeys = {
      userrk: 'bypasslist:customlist',
      poprk: 'bypasslist:popularrules'
    };
    this.enabledRules = new Map([['privatenetworks', ['0.0.0.0/8', '10.0.0.0/8', '127.0.0.0/8', '169.254.0.0/16', '192.168.0.0/16', '172.16.0.0/12', '::1', 'localhost', '*.local']], ['pinggateways', this.generatePingGateways()], [this.storageKeys.userrk, []], [this.storageKeys.poprk, []]]);
    this.netflixBypassRules = ['https://netflix.com', 'https://*.netflix.com', 'https://*.nflxvideo.net', 'https://*.nflximg.net'];
    this.huluBypassRules = ['https://*.hulu.com', 'https://*.hulustream.com'];
    this.popularRules = Object.freeze(new Map([['netflix', this.netflixBypassRules], ['hulu', this.huluBypassRules]]));
  }

  static trimUserRules(rules) {
    return rules.map(e => {
      return e.trim();
    }).filter(e => {
      return e.length > 0;
    });
  }

  init() {
    const {
      userrk,
      poprk
    } = this.storageKeys;

    if (this.storage.hasItem(userrk) && this.storage.getItem(userrk).length > 0) {
      this.setUserRules(this.storage.getItem(userrk).split(','));
    }

    if (this.storage.hasItem(poprk) && this.storage.getItem(poprk).length > 0) {
      this.storage.getItem(poprk).split(',').forEach(name => {
        return this.enablePopularRule(name);
      });
    }
  }

  resetPopularRules() {
    // turn off all popular rules
    this.popularRulesByName().map(rule => {
      return this.disablePopularRule(rule, true);
    }); // turn on popular and user rules from storage

    const {
      userrk,
      poprk
    } = this.storageKeys;

    if (this.storage.hasItem(poprk) && this.storage.getItem(poprk).length > 0) {
      this.storage.getItem(poprk).split(',').forEach(name => {
        this.enablePopularRule(name, true);
      });
    }

    if (this.storage.hasItem(userrk)) {
      this.setUserRules(this.storage.getItem(userrk).split(','), true);
    }
  }

  generatePingGateways() {
    const {
      util: {
        regionlist
      }
    } = this.app;
    const http = regionlist.toArray().map(r => {
      return `http://${r.host}:8888`;
    });
    const https = regionlist.toArray().map(r => {
      return `https://${r.host}:8888`;
    });
    return http.concat(https);
  }

  updatePingGateways() {
    this.enabledRules.set('pinggateways', this.generatePingGateways());

    if (this.app.proxy.enabled()) {
      this.app.proxy.enable();
    }
  }

  isRuleEnabled(ruleName) {
    return this.enabledRules.has(ruleName);
  }

  popularRulesByName() {
    return Array.from(this.popularRules.keys());
  }

  visibleSize() {
    return this.getUserRules().length + this.enabledPopularRules().length;
  }

  async restartProxy(cb = () => {}) {
    const {
      proxy
    } = this.app;

    if (!proxy) {
      throw new Error(debug('proxy not ready'));
    }

    if (proxy.enabled()) {
      await proxy.enable().then(cb);
    } else {
      await Promise.resolve(cb());
    }
  }

  getUserRules() {
    return BypassList.trimUserRules(Array.from(this.enabledRules.get(this.storageKeys.userrk)));
  }

  setUserRules(rules, bridged) {
    const {
      adapter
    } = this.app;
    this.storage.setItem(this.storageKeys.userrk, BypassList.trimUserRules(Array.from(rules)).join(','));
    this.enabledRules.set(this.storageKeys.userrk, rules);

    if (!bridged && typeof browser != 'undefined') {
      adapter.sendMessage('setUserRules', rules);
    }

    return this.getUserRules();
  }

  getRulesSmartLoc() {
    const {
      helpers
    } = app;
    const bypassRules = this.enabledRules.get(this.storageKeys.userrk);
    const rules = bypassRules.map((v, k) => {
      if (helpers.UrlParser.parse(v)) {
        return helpers.UrlParser.parse(v).domain;
      }
    });
    return rules;
  }

  addUserRule(string, restartProxy = false) {
    let userString = string;

    if (userString.endsWith('/')) {
      userString = string.substring(0, string.length - 1);
    }

    const userRules = this.getUserRules();
    userRules.push(userString);
    this.setUserRules([...new Set(userRules)]);

    if (restartProxy) {
      this.restartProxy();
    }
  }

  removeUserRule(string, restartProxy = false) {
    let userString = string;

    if (userString.endsWith('/')) {
      userString = string.substring(0, string.length - 1);
    }

    const rules = this.getUserRules();
    this.setUserRules(rules.filter(e => {
      return e !== userString;
    }));

    if (restartProxy) {
      this.restartProxy();
    }
  }

  enablePopularRule(name, bridged, restartProxy = true) {
    if (!this.popularRulesByName().includes(name)) {
      return Promise.reject(new Error(`${name} is not a valid popular rule`));
    }

    if (this.enabledPopularRules().includes(name)) {
      return Promise.resolve();
    }

    const {
      adapter
    } = this.app;
    return new Promise(resolve => {
      // enable rule
      this.enabledRules.set(name, this.popularRules.get(name)); // ensure mock app is aware of this change
      // TODO: send the restartProxy params over to adapter

      if (!bridged && typeof browser != 'undefined') {
        return resolve(adapter.sendMessage('enablePopularRule', {
          name,
          restartProxy
        }));
      }

      return resolve();
    }).then(() => {
      if (!this.foreground && restartProxy) {
        return this.restartProxy();
      }

      return Promise.resolve();
    }).then(() => {
      this.storage.setItem(this.storageKeys.poprk, this.enabledPopularRules().join(','));
      debug(`bypasslist: added ${name}`);
    });
  }

  disablePopularRule(name, bridged, restartProxy = true) {
    if (!this.popularRulesByName().includes(name)) {
      return Promise.reject(new Error(`no such popular rule: ${name}`));
    }

    if (!this.enabledPopularRules().includes(name)) {
      return Promise.resolve();
    }

    const {
      adapter
    } = this.app;
    return new Promise(resolve => {
      // disable rule
      this.enabledRules.delete(name); // ensure mock app is aware of this change

      if (!bridged && typeof browser != 'undefined') {
        return resolve(adapter.sendMessage('disablePopularRule', {
          name,
          restartProxy
        }));
      }

      return resolve();
    }).then(() => {
      if (!this.foreground && restartProxy) {
        this.restartProxy();
      }
    }).then(() => {
      this.storage.setItem(this.storageKeys.poprk, this.enabledPopularRules().join(','));
      debug(`bypasslist: removed ${name}`);
    });
  }

  enabledPopularRules() {
    const enabledRulesByName = Array.from(this.enabledRules.keys());
    const popularRulesByName = this.popularRulesByName();
    return popularRulesByName.filter(name => {
      return enabledRulesByName.includes(name);
    });
  }

  toArray() {
    const rules = [...Array.from(this.enabledRules.values())];
    return [].concat(...rules.map(r => {
      return typeof r === 'function' ? r() : r;
    }));
  }
  /**
   * Create a file containing the current ruleset and download it on client
   *
   * @returns {void}
   */


  saveRulesToFile() {
    if (this.foreground && typeof browser != 'undefined') {
      const {
        adapter
      } = this.app;
      adapter.sendMessage(_helpers_messagingFirefox__WEBPACK_IMPORTED_MODULE_0__["Type"].DOWNLOAD_BYPASS_JSON);
    } else {
      const payload = JSON.stringify({
        popularRules: this.enabledPopularRules(),
        userRules: this.getUserRules()
      });
      const file = new File('application/json', [payload]);
      file.download('bypass-rules.json');
    }
  }
  /**
   * Import the specified rule sets into the application
   *
   * @param {object} rules Set of rules to import
   * @returns {void}
   */


  importRules({
    userRules,
    popularRules
  }) {
    const importRuleSet = (importedRules, getRules, enableRule, disableRule) => {
      if (Array.isArray(importedRules)) {
        // Disable rules not in importedRules
        getRules().forEach(rule => {
          if (!importedRules.includes(rule)) {
            disableRule(rule);
          }
        }); // Enable importedRules

        importedRules.forEach(enableRule);
      } // Disable all rules
      else if (typeof importedRules === 'undefined') {
          getRules().forEach(disableRule);
        } else {
          debug('rule set is invalid type, expected array');
        }
    };

    try {
      importRuleSet(userRules, this.getUserRules, name => {
        return this.addUserRule(name, false);
      }, name => {
        return this.removeUserRule(name, false);
      });
      importRuleSet(popularRules, this.enabledPopularRules, name => {
        return this.enablePopularRule(name, false);
      }, name => {
        return this.disablePopularRule(name, false);
      });
      this.restartProxy();
    } catch (err) {
      debug(`failed to update rules with error: ${err}`);
    }
  }
  /**
   * Create a new popup window for importing rules file
   *
   * @returns {Promise<void>}
   */


  spawnImportTab() {
    // eslint-disable-line class-methods-use-this
    chrome.tabs.create({
      url: chrome.runtime.getURL('html/popups/importrules.html')
    });
  }

}

/***/ }),
/* 127 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var _helpers_http__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(15);
/* harmony import */ var _helpers_compare__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(97);


/**
 * LatencyManager
 * ==============
 *
 * Responsible for managing the `latency` field for regions.
 *
 * "round" - record RTT for single request to region
 * "test" -  perform ${ROUNDS} rounds consecutively
 * "run" - perform ${MAX_CONCURRENT} tests concurrently
 */

class LatencyManager {
  static get MAX_CONCURRENT() {
    return 24;
  }

  static get ROUNDS() {
    return 3;
  }

  constructor(app) {
    this.app = app;
    this.run = this.run.bind(this);
  }

  get regionlist() {
    return this.app.util.regionlist;
  }
  /**
   * Runs the latency tests
   *
   * @return {Promise} resolves when tests complete
   */


  async run() {
    const {
      regionlist
    } = this;
    const start = performance.now();
    const queue = regionlist.toArray();
    const tests = LatencyManager.array(LatencyManager.MAX_CONCURRENT).map(() => {
      return LatencyManager.runTest({
        queue,
        regionlist
      });
    });
    await Promise.all(tests);
    const end = performance.now();
    const duration = Math.floor(end - start);
    debug(`latencymanager.js: finished latency tests in ${duration}ms`);
  }

  static async round(region) {
    try {
      const start = performance.now();
      await _helpers_http__WEBPACK_IMPORTED_MODULE_0__[/* default */ "a"].head(`http://${region.ping}:8888/ping.txt`);
      const end = performance.now();
      const duration = Math.floor(end - start);
      return duration;
    } catch (err) {
      return 'ERROR';
    }
  }

  static async runTest({
    queue,
    regionlist
  }) {
    const region = queue.pop();
    if (!region) return Promise.resolve();
    const results = [];

    for (let i = 0; i < LatencyManager.ROUNDS; i++) {
      results.push(await LatencyManager.round(region));
    }

    const latency = results.sort(_helpers_compare__WEBPACK_IMPORTED_MODULE_1__[/* byLatency */ "a"]).shift();
    regionlist.updateRegion({ ...region,
      latency
    });
    return LatencyManager.runTest({
      queue,
      regionlist
    });
  }

  static array(size) {
    return [...Array(size)];
  }

}

/* harmony default export */ __webpack_exports__["a"] = (LatencyManager);

/***/ }),
/* 128 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
class PlatformInfo {
  constructor(app) {
    // bindings
    this.isWindows = this.isWindows.bind(this);
    this.lineEnding = this.lineEnding.bind(this);
    this.init = this.init.bind(this); // init

    this.app = app;
    this.os = undefined;
    this.arch = undefined;
    this.naclArch = undefined;
    this.ready = false;
    this.initializing = this.init();
  }

  init() {
    return new Promise((resolve, reject) => {
      // eslint-disable-next-line camelcase
      chrome.runtime.getPlatformInfo(({
        os,
        arch,
        nacl_arch
      }) => {
        if (chrome.runtime.lastError) {
          reject(chrome.runtime.lastError);
        } else {
          this.os = os;
          this.arch = arch; // eslint-disable-next-line camelcase

          this.naclArch = nacl_arch;
          this.ready = true;
          resolve();
        }
      });
    });
  }

  isWindows() {
    return this.os === 'win';
  }

  lineEnding() {
    return this.isWindows() ? '\r\n' : '\n';
  }

}

/* harmony default export */ __webpack_exports__["a"] = (PlatformInfo);

/***/ }),
/* 129 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var _helpers_compare__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(97);


class RegionSorter {
  constructor(app) {
    this.app = app;
    this.nameSort = this.nameSort.bind(this);
    this.latencySort = this.latencySort.bind(this);
  } // eslint-disable-next-line class-methods-use-this


  nameSort(regions) {
    return regions.sort((a, b) => {
      return a.name.localeCompare(b.name);
    });
  } // eslint-disable-next-line class-methods-use-this


  latencySort(regions) {
    return regions.sort((a, b) => {
      return _helpers_compare__WEBPACK_IMPORTED_MODULE_0__[/* byLatency */ "a"](a.latency, b.latency);
    });
  }

}

/* harmony default export */ __webpack_exports__["a"] = (RegionSorter);

/***/ }),
/* 130 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
function clear(csettings) {
  Object.values(csettings).filter(s => {
    return s.isAvailable ? s.isAvailable() : true;
  }).filter(s => {
    return !s.alwaysActive;
  }).forEach(s => {
    s.clearSetting();
  });
}

function apply(csettings, settings) {
  Object.values(csettings).filter(s => {
    return s.isAvailable ? s.isAvailable() : true;
  }).filter(s => {
    return settings.getItem(s.settingID);
  }).forEach(s => {
    s.applySetting();
  });
}

class SettingsMananger {
  constructor(app) {
    this.app = app;
    this.enable = this.enable.bind(this);
    this.reapply = this.reapply.bind(this);
    this.disable = this.disable.bind(this);
  }

  enable() {
    const {
      app: {
        util: {
          settings
        },
        chromesettings,
        contentsettings
      }
    } = this;
    apply(contentsettings, settings);
    apply(chromesettings, settings);
  }

  clearAndReapplySettings() {
    const {
      app: {
        util: {
          settings
        },
        proxy
      }
    } = this;
    const alwaysActive = settings.getItem('alwaysActive');
    const proxyValue = proxy.enabled() == 'fixed_servers' || proxy.enabled() == 'pac_script' ? true : false;
    const boolArray = [alwaysActive, proxyValue];
    boolArray.includes(true) ? this.enable() : this.disable();
  }
  /*
     The purpose of this function is to deal with a Chrome bug where when one content setting
     is cleared, all other content settings are also cleared! (eg camera.clear() will clear
     microphone too). The property `microphone.isApplied()` will still be true but
     `camera.isApplied()` won't, so it can be used to determine if the setting should be
     reapplied again or not.
       Link to Chrome Bug: https://bugs.chromium.org/p/chromium/issues/detail?id=700404#c18
     This issue has been fixed in Chrome on Sept 21 2018.
     Will keep this method around until at lesat 5 versions have passed.
     Current Chrome Version: Version 69.0.3497.100 (Official Build) (64-bit)
       After 5 versions have passed, add conditional code to only run the reapply method if the
     version detected is older than Chrome version 71 (assume fix lands in that build).
  */


  reapply(contentsettings) {
    const {
      app: {
        util: {
          settings
        }
      }
    } = this;
    const enabled = settings.enabled();
    Object.values(contentsettings).filter(s => {
      return s.isAvailable ? s.isAvailable() : true;
    }).filter(s => {
      return s.isApplied();
    }).filter(s => {
      return enabled || s.alwaysActive;
    }).forEach(s => {
      s.applySetting();
    });
  }

  disable() {
    const {
      app: {
        contentsettings,
        chromesettings
      }
    } = this;
    clear(chromesettings);
    clear(contentsettings);
    this.reapply(contentsettings);
  }

}

/* harmony default export */ __webpack_exports__["a"] = (SettingsMananger);

/***/ }),
/* 131 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return SmartLocation; });
class SmartLocation {
  constructor(app, foreground) {
    // Bindings
    this.app = app;
    this.init = this.init.bind(this);
    this.storage = app.util.storage;
    this.helpers = app.helpers;
    this.regionlist = app.util.regionlist;
    this.proxy = app.proxy;
    this.adapter = app.adapter;
    this.foreground = foreground;
    this.userRules = null;
    this.checkSmartLocation = null;
    this.currentTabUrl = '';
    this.setCurrentDomain = this.setCurrentDomain.bind(this);
    this.visibleSize = this.visibleSize.bind(this);
    this.removeSmartLocation = this.removeSmartLocation.bind(this);
    this.getSmartLocationRules = this.getSmartLocationRules.bind(this);
  }

  init() {
    try {
      //init userrules array and smartlocation check
      if (!this.storage.getItem('smartLocationRules')) {
        this.storage.setItem("smartLocationRules", JSON.stringify([]));
        this.storage.setItem("checkSmartLocation", false);
      }

      const smartLocationRules = this.storage.getItem('smartLocationRules');

      if (typeof smartLocationRules != 'string') {
        this.storage.setItem("smartLocationRules", JSON.stringify(smartLocationRules));
      }

      this.userRules = typeof smartLocationRules == 'string' ? JSON.parse(smartLocationRules) : smartLocationRules;
      this.checkSmartLocation = this.storage.getItem('checkSmartLocation');
    } catch (err) {
      this.storage.setItem("smartLocationRules", JSON.stringify([]));
      this.storage.setItem("checkSmartLocation", false);
      debug(err);
    }
  }

  visibleSize() {
    return JSON.parse(this.storage.getItem('smartLocationRules')).length;
  }

  setCurrentDomain() {
    chrome.tabs.query({
      currentWindow: true,
      active: true
    }, ([tab]) => {
      if (tab) {
        const url = this.helpers.UrlParser.parse(tab.url) ? this.helpers.UrlParser.parse(tab.url) : '';
        this.currentTabUrl = !tab.url.startsWith('chrome://') ? url.domain : null;
      }
    });
  }

  addSmartLocation(userRules, userSelect) {
    const regionList = this.regionlist.getRegions(); //add smsart location

    let usersRules = JSON.parse(this.storage.getItem('smartLocationRules')) ? JSON.parse(this.storage.getItem('smartLocationRules')) : [];
    const smartRule = {
      userRules,
      userSelect,
      proxy: Object.values(regionList).filter(v => v.id == userSelect)[0]
    };

    if (smartRule.proxy) {
      usersRules.push(smartRule);
      this.saveToStorage("smartLocationRules", usersRules);
    }
  }

  removeSmartLocation(rule) {
    //remove smart location
    let usersRules = JSON.parse(this.storage.getItem('smartLocationRules')) ? JSON.parse(this.storage.getItem('smartLocationRules')) : [];
    usersRules = usersRules.filter(v => v.userRules != rule.userRules);
    this.saveToStorage("smartLocationRules", usersRules);

    if (typeof browser == 'undefined') {
      this.app.proxy.filterByRemovedLocation(rule);
    }
  }

  editSmartLocation(rule) {
    const regionList = this.regionlist.getRegions();
    const userRules = JSON.parse(this.storage.getItem('smartLocationRules'));
    rule.proxy = Object.values(regionList).filter(v => v.id == rule.userSelect)[0];

    if (rule.proxy) {
      userRules.splice(rule.indexEdit, 1, rule);
      delete rule.indexEdit;
      this.saveToStorage("smartLocationRules", userRules);
    }
  }

  getSmartLocationRules(value) {
    const userRules = typeof this.storage.getItem(value) == 'string' ? JSON.parse(this.storage.getItem(value)) : this.storage.getItem(value);
    return userRules;
  }

  saveToStorage(key, value) {
    if (this.foreground && typeof browser != 'undefined') {
      this.adapter.sendMessage('smartLocation', {
        settingID: key,
        value: value
      });
    }

    return this.storage.setItem(key, JSON.stringify(value));
  }

}

/***/ }),
/* 132 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var _helpers_http__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(15);
/* harmony import */ var _helpers_reportError__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(64);
/* harmony import */ var _helpers_timer__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(76);
/*
   IMPORTANT
   =========

   Sending too many requests to `privateinternetaccess.com` results
   in increased DNS costs.

   Current Approach
   ----------------

   Run updates:
   1) before proxy connects (real ip)
   2) after proxy connects (proxy ip)
   3) after proxy disconnects (real ip)
 */




class IpManager {
  constructor(app) {
    // bindings
    this.getRealIP = this.getRealIP.bind(this);
    this.getProxyIP = this.getProxyIP.bind(this);
    this.updateIpByRegion = this.updateIpByRegion.bind(this);
    this.updateByCountry = this.updateByCountry.bind(this); // init

    this.app = app;
    this.realIP = null;
    this.proxyIP = null;
  }

  getRealIP() {
    return this.realIP;
  }

  getProxyIP() {
    return this.proxyIP;
  }

  getIPs() {
    return {
      realIP: this.getRealIP(),
      proxyIP: this.getProxyIP()
    };
  }

  updateIpByRegion(tab) {
    const location = this.app.util.regionlist.getRegionById(tab.customCountry);

    if (location && this.app.proxy.getEnabled()) {
      this.proxyIP = location.ping;
    } else {
      if (typeof browser == 'undefined') {
        const region = this.app.util.regionlist.getSelectedRegion();
        this.updateByCountry(region);
      } else {
        this.update({
          retry: true
        });
      }
    }
  }

  updateByCountry(country) {
    if (country) {
      this.proxyIP = country.ping;
      this.app.util.icon.online(country);
    }
  }
  /**
   * Update an IP
   *
   * If proxy currently connected, will update proxyIP
   * If proxy current disconnected, will update realIP
   *
   * Recommended not to await this method if retry is enabled
   *
   * @param {*} opts
   * @param {boolean} retry whether to retry on failure (takes up to 7mins)
   */


  async update({
    retry = false
  } = {}) {
    const {
      util: {
        storage,
        icon,
        settingsmanager
      }
    } = this.app;
    debug('ipmanager: updating ip address');
    let attempt = 0;
    const maxAttempts = retry ? 10 : 0;

    const attemptUpdate = async () => {
      const date = new Date().getTime();
      const url = `https://www.privateinternetaccess.com/api/client/services/https/status?${date}`;
      const res = await _helpers_http__WEBPACK_IMPORTED_MODULE_0__[/* default */ "a"].get(url);
      const info = await res.json();
      const online = storage.getItem('online');
      const {
        ip
      } = info;
      let {
        connected
      } = info;
      connected = String(connected) === 'true';
      console.log('onlineonlineonlineonlineonlineonline ', online);
      console.log('info ', info);
      const onlineProxy = typeof browser == "undefined" ? online : Boolean(online);

      if (online.toString() == 'true') {
        this.proxyIP = ip;
      } else {
        this.realIP = ip;
        this.proxyIP = null;
      }

      if (typeof browser == 'undefined') {
        this.app.courier.sendMessage('refresh');
      }
    };

    while (attempt <= maxAttempts) {
      await Object(_helpers_timer__WEBPACK_IMPORTED_MODULE_2__[/* default */ "a"])(attempt ** 2 * 1000);

      try {
        await attemptUpdate();
        break;
      } catch (err) {
        Object(_helpers_reportError__WEBPACK_IMPORTED_MODULE_1__[/* default */ "a"])('ipmanager', err);
      }

      attempt += 1;
    }
  }

}

/* harmony default export */ __webpack_exports__["a"] = (IpManager);

/***/ }),
/* 133 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var _firefoxsettings_chromesetting__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(16);


class WebRTC extends _firefoxsettings_chromesetting__WEBPACK_IMPORTED_MODULE_0__[/* default */ "a"] {
  constructor() {
    super(WebRTC.getSetting()); // functions

    this.applySetting = this.createApplySetting('proxy_only', 'webrtc', 'block');
    this.clearSetting = this.createClearSetting('webrtc', 'unblock'); // bindings

    this.onChange = this.onChange.bind(this); // init

    this.settingDefault = false;
    this.blockable = Boolean(this.setting);
    this.settingID = 'preventwebrtcleak';
  }

  onChange(details) {
    this.setLevelOfControl(details.levelOfControl);
    this.setBlocked(details.value === 'proxy_only');
  }

  static getSetting() {
    if (chrome.privacy && chrome.privacy.network) {
      return chrome.privacy.network.webRTCIPHandlingPolicy;
    }

    return undefined;
  }

}

/* harmony default export */ __webpack_exports__["a"] = (WebRTC);

/***/ }),
/* 134 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var _firefoxsettings_chromesetting__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(16);


class HttpReferrer extends _firefoxsettings_chromesetting__WEBPACK_IMPORTED_MODULE_0__[/* default */ "a"] {
  constructor() {
    super(HttpReferrer.getSetting()); // functions

    this.applySetting = this.createApplySetting(false, 'httpreferer', 'block');
    this.clearSetting = this.createClearSetting('httpreferer', 'unblock'); // bindings

    this.onChange = this.onChange.bind(this); // init

    this.settingDefault = false;
    this.settingID = 'blockreferer';
    this.referable = Boolean(this.setting);
  }

  onChange(details) {
    this.setLevelOfControl(details.levelOfControl);
    this.setBlocked(details.value === false);
  }

  static getSetting() {
    if (chrome.privacy && chrome.privacy.websites) {
      return chrome.privacy.websites.referrersEnabled;
    }

    return undefined;
  }

}

/* harmony default export */ __webpack_exports__["a"] = (HttpReferrer);

/***/ }),
/* 135 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var _firefoxsettings_chromesetting__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(16);


class HyperLinkAudit extends _firefoxsettings_chromesetting__WEBPACK_IMPORTED_MODULE_0__[/* default */ "a"] {
  constructor() {
    super(HyperLinkAudit.getSetting()); // function

    this.applySetting = this.createApplySetting(false, 'hyperlinkaudit', 'block');
    this.clearSetting = this.createClearSetting('hyperlinkaudit', 'unblock'); // bindings

    this.onChange = this.onChange.bind(this); // init

    this.settingDefault = false;
    this.available = Boolean(this.setting);
    this.settingID = 'blockhyperlinkaudit';
  }

  onChange(details) {
    this.setLevelOfControl(details.levelOfControl);
    this.setBlocked(details.value === false);
  }

  static getSetting() {
    if (chrome.privacy && chrome.privacy.websites) {
      return chrome.privacy.websites.hyperlinkAuditingEnabled;
    }

    return undefined;
  }

}

/* harmony default export */ __webpack_exports__["a"] = (HyperLinkAudit);

/***/ }),
/* 136 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var _firefoxsettings_chromesetting__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(16);


class NetworkPredication extends _firefoxsettings_chromesetting__WEBPACK_IMPORTED_MODULE_0__[/* default */ "a"] {
  constructor() {
    super(NetworkPredication.getSetting()); // functions

    this.applySetting = this.createApplySetting(false, 'networkprediction', 'block');
    this.clearSetting = this.createClearSetting('networkprediction', 'unblock'); // bindings

    this.onChange = this.onChange.bind(this); // init

    this.settingDefault = false;
    this.available = Boolean(this.setting);
    this.settingID = 'blocknetworkprediction';
  }

  onChange(details) {
    this.setLevelOfControl(details.levelOfControl);
    this.setBlocked(details.value === false);
  }

  static getSetting() {
    if (chrome.privacy && chrome.privacy.network) {
      return chrome.privacy.network.networkPredictionEnabled;
    }

    return undefined;
  }

}

/* harmony default export */ __webpack_exports__["a"] = (NetworkPredication);

/***/ }),
/* 137 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var _firefoxsettings_chromesetting__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(16);


class TrackingProtection extends _firefoxsettings_chromesetting__WEBPACK_IMPORTED_MODULE_0__[/* default */ "a"] {
  constructor() {
    super(TrackingProtection.getSetting()); // functions

    this.applySetting = this.createApplySetting('always', 'trackingprotection', 'block'); // bindings

    this.clearSetting = this.clearSetting.bind(this);
    this.onChange = this.onChange.bind(this); // init

    this.settingDefault = false;
    this.available = Boolean(this.setting);
    this.settingID = 'trackingprotection';
  }

  async clearSetting() {
    try {
      await this.set({
        value: false
      }, {
        applyValue: true
      });
      _firefoxsettings_chromesetting__WEBPACK_IMPORTED_MODULE_0__[/* default */ "a"].debug('trackingprotection', 'unblock ok');
    } catch (err) {
      _firefoxsettings_chromesetting__WEBPACK_IMPORTED_MODULE_0__[/* default */ "a"].debug('trackingprotection', 'unblock failed', err);
    }

    return this;
  }

  onChange(details) {
    this.setLevelOfControl(details.levelOfControl);
    this.setBlocked(details.value === 'always');
  }

  static getSetting() {
    if (chrome.privacy && chrome.privacy.websites) {
      return chrome.privacy.websites.trackingProtectionMode;
    }

    return undefined;
  }

}

/* harmony default export */ __webpack_exports__["a"] = (TrackingProtection);

/***/ }),
/* 138 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var _firefoxsettings_chromesetting__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(16);


class FingerprintProtection extends _firefoxsettings_chromesetting__WEBPACK_IMPORTED_MODULE_0__[/* default */ "a"] {
  constructor() {
    super(FingerprintProtection.getSetting()); // functions

    this.applySetting = this.createApplySetting(true, 'fingerprintprotection', 'block'); // bindings

    this.clearSetting = this.clearSetting.bind(this);
    this.onChange = this.onChange.bind(this); // init

    this.settingDefault = false;
    this.available = Boolean(this.setting);
    this.settingID = 'fingerprintprotection';
  }

  async clearSetting() {
    try {
      await this.set({
        value: false
      }, {
        applyValue: true
      });
      _firefoxsettings_chromesetting__WEBPACK_IMPORTED_MODULE_0__[/* default */ "a"].debug('fingerprintprotection', 'unblock ok');
    } catch (err) {
      _firefoxsettings_chromesetting__WEBPACK_IMPORTED_MODULE_0__[/* default */ "a"].debug('fingerprintprotection', 'unblock failed', err);
    }

    return this;
  }

  onChange(details) {
    this.setLevelOfControl(details.levelOfControl);
    this.setBlocked(details.value === false);
  }

  static getSetting() {
    if (chrome.privacy && chrome.privacy.websites) {
      return chrome.privacy.websites.resistFingerprinting;
    }

    return undefined;
  }

}

/* harmony default export */ __webpack_exports__["a"] = (FingerprintProtection);

/***/ }),
/* 139 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
class UrlParser {
  constructor() {
    this.parse = this.parse.bind(this);
  }

  parse(url) {
    const match = url.match(/^(http|https|ftp)?(?:[\:\/]*)([a-z0-9\.-]*)(?:\:([0-9]+))?(\/[^?#]*)?(?:\?([^#]*))?(?:#(.*))?$/i);
    const ret = {
      protocol: '',
      host: '',
      port: '',
      path: '',
      query: '',
      fragment: '',
      domain: '',
      subdomain: ''
    };

    if (!match) {
      return ret;
    }

    if (match[1]) {
      ret.protocol = match[1];
    }

    if (match[2]) {
      ret.host = match[2];
    }

    if (match[3]) {
      ret.port = match[3];
    }

    if (match[4]) {
      ret.path = match[4];
    }

    if (match[5]) {
      ret.query = match[5];
    }

    if (match[6]) {
      ret.fragment = match[6];
    }

    if (ret.host) {
      const splitDomanin = match[2].split('.');

      if (splitDomanin.length == 3) {
        ret.domain = splitDomanin[1] + '.' + splitDomanin[2];
        ret.subdomain = splitDomanin[0];
      } else {
        ret.domain = splitDomanin[0] + '.' + splitDomanin[1];
      }
    }

    return ret;
  }

}

/* harmony default export */ __webpack_exports__["a"] = (UrlParser);

/***/ }),
/* 140 */,
/* 141 */,
/* 142 */,
/* 143 */,
/* 144 */,
/* 145 */,
/* 146 */
/***/ (function(module, exports, __webpack_require__) {

/* eslint-disable
    consistent-return,
    no-bitwise,
    no-plusplus,
    no-restricted-syntax,
    no-underscore-dangle,
    no-unused-vars,
    no-use-before-define,
*/
const config = __webpack_require__(107);

const util = __webpack_require__(109);

const data = {
  localDomains: config.get().localDomains,
  nodeOverrides: config.get().nodeOverrides,
  IPv4NotationRE: /^\d+\.\d+\.\d+\.\d+$/g,
  localIPsRE: /(^127\.)|(^192\.168\.)|(^10\.)|(^172\.1[6-9]\.)|(^172\.2[0-9]\.)|(^172\.3[0-1]\.)/
};
module.exports = {
  data,

  // Merge additional hosts from ruleOverrides into rules based on the domain.
  mergeRuleOverrides(rules, overrides) {
    if (!((rules ? rules.length : undefined) > 0)) {
      return [];
    }

    if (!((overrides ? overrides.length : undefined) > 0)) {
      return rules;
    }

    for (const rule of rules) {
      for (const override of overrides) {
        if (override.domains.indexOf(rule.domain) > -1) {
          // We have a match, concatenate hosts with de-duplication
          rule.hosts = util.concatUnique(rule.hosts || [], override.hosts || []);
        }
      }
    }

    return rules;
  },

  /* Helper functions used by us and and the proxy pacscript */
  // Returns a concatenated string of proxy nodes based on country code
  nodeLookup(nodeDict, cc) {
    return nodeDict[cc] || false;
  },

  // Helper function to compare a host against an array of hosts with matchWildcardDomain
  compareHosts(hosts, host) {
    for (const h of hosts) {
      if (this.matchWildcardDomain(host, h)) {
        return h;
      }
    }
  },

  // Helper function to compare a URL against an array of regexp URL patterns
  compareURLs(patterns, url) {
    for (const p of patterns) {
      if (p.test(url)) {
        return p;
      }
    }
  },

  // WARNING: The pattern facebook.com will match the host fakefacebook.com
  // It's safer to use matchWildcardDomain instead.
  dnsDomainIs(host, pattern) {
    return host.length >= pattern.length && host.substring(host.length - pattern.length) === pattern;
  },

  // To make it easier for users we match all subdomains of a domain as well
  // E.g. the host images.facebook.com does match if the domain is facebook.com
  // NOTE: See here before optimizing: http://codepen.io/berstend/pen/wBjBaL
  matchWildcardDomain(host, domain) {
    const exactMatch = host === domain; // Check if the host ends with the supplied domain

    const tldMatch = host.slice(-domain.length) === domain; // Check if the character before the domain is a dot

    const hasSubdomain = host[host.lastIndexOf(domain) - 1] === '.';
    return exactMatch || tldMatch && hasSubdomain;
  },

  // Returns alternative proxy nodes (e.g. 'US-ALT1') if an override is matching the location and host.
  matchNodeOverride(host, cc) {
    const result = this.data.nodeOverrides.find(o => o.target_cc === cc && this.compareHosts(o.hosts, host));
    return result ? result.nodes : false;
  },

  // Generic support for custom, user defined rules
  // Returns the index of the rule if there there is a match
  matchRules(rules, host, url) {
    if (!rules || !rules.length) {
      return;
    } // In exportPAC we pre-populate rulesWithOverrides for speed reasons, we don't during background usage.
    // Again: The following assignment is not executed in the proxy.pac context.


    if (!this.data.rulesWithOverrides) {
      rules = this.mergeRuleOverrides(rules, config.get().ruleOverrides);
    } // Loop through all rules and check if they match


    for (let i = 0; i < rules.length; i++) {
      const rule = rules[i];

      if (this.matchWildcardDomain(host, rule.domain) || rule.hosts && this.compareHosts(rule.hosts, host)) {
        return i;
      }
    }
  },

  // NOTE: We start simple and only support domain and host matching for now.
  // or (url? and @compareURLs(rule.urls, url)))
  // and not (rule.excludes and @compareURLs(rule.excludes, url))

  /*
    _getProxyState is the main function determining the proxy state of a given url and host.
    @param {string} url URL to test (rarely used)
    @param {string} host Host to test
    @param {array} rules The user defined custom rules
    @return {string} LOCAL, DIRECT, DEFAULT or $COUNTRYCODE (e.g. DE or OFF)
  */
  _getProxyState(url, host, rules) {
    // No need to lowercase host, see http://findproxyforurl.com/misconceptions/
    url = url.toLowerCase(); // Reset the lastIndex regex property which is cached for subsequent calls
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/RegExp/lastIndex

    this.data.IPv4NotationRE.lastIndex = 0;
    this.data.localIPsRE.lastIndex = 0; // Custom IPv6 compatible isPlainHostName replacement functionality
    // Returns true if host is not an IP nor FQDN, e.g. http://intranet

    if (!~host.indexOf('.') && !~host.indexOf(':')) {
      return 'LOCAL';
    } // Check if host is a local IPv4 address


    if (this.data.IPv4NotationRE.test(host) && this.data.localIPsRE.test(host)) {
      return 'LOCAL';
    }

    for (const local of this.data.localDomains) {
      if (this.matchWildcardDomain(host, local)) {
        return 'LOCAL';
      }
    }

    const match = this.matchRules(rules, host, url);

    if (Number.isInteger(match)) {
      return rules[match].cc;
    }

    return 'DEFAULT';
  }

};

/***/ }),
/* 147 */
/***/ (function(module, exports, __webpack_require__) {

__webpack_require__(148);
__webpack_require__(150);
__webpack_require__(151);
__webpack_require__(152);
__webpack_require__(153);
__webpack_require__(154);
__webpack_require__(155);
__webpack_require__(156);
__webpack_require__(157);
__webpack_require__(158);
__webpack_require__(159);
__webpack_require__(160);
__webpack_require__(161);
__webpack_require__(162);
__webpack_require__(163);
__webpack_require__(165);
__webpack_require__(167);
__webpack_require__(169);
__webpack_require__(170);
__webpack_require__(172);
__webpack_require__(173);
__webpack_require__(55);
__webpack_require__(56);
__webpack_require__(57);
__webpack_require__(58);
__webpack_require__(174);
__webpack_require__(175);
__webpack_require__(176);
__webpack_require__(177);
module.exports = __webpack_require__(18).Object;


/***/ }),
/* 148 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

// ECMAScript 6 symbols shim
var global = __webpack_require__(3);
var has = __webpack_require__(19);
var DESCRIPTORS = __webpack_require__(5);
var $export = __webpack_require__(2);
var redefine = __webpack_require__(30);
var META = __webpack_require__(94).KEY;
var $fails = __webpack_require__(11);
var shared = __webpack_require__(32);
var setToStringTag = __webpack_require__(45);
var uid = __webpack_require__(31);
var wks = __webpack_require__(6);
var wksExt = __webpack_require__(63);
var wksDefine = __webpack_require__(62);
var enumKeys = __webpack_require__(149);
var isArray = __webpack_require__(43);
var anObject = __webpack_require__(17);
var isObject = __webpack_require__(8);
var toObject = __webpack_require__(9);
var toIObject = __webpack_require__(14);
var toPrimitive = __webpack_require__(20);
var createDesc = __webpack_require__(29);
var _create = __webpack_require__(48);
var gOPNExt = __webpack_require__(110);
var $GOPD = __webpack_require__(28);
var $GOPS = __webpack_require__(95);
var $DP = __webpack_require__(10);
var $keys = __webpack_require__(26);
var gOPD = $GOPD.f;
var dP = $DP.f;
var gOPN = gOPNExt.f;
var $Symbol = global.Symbol;
var $JSON = global.JSON;
var _stringify = $JSON && $JSON.stringify;
var PROTOTYPE = 'prototype';
var HIDDEN = wks('_hidden');
var TO_PRIMITIVE = wks('toPrimitive');
var isEnum = {}.propertyIsEnumerable;
var SymbolRegistry = shared('symbol-registry');
var AllSymbols = shared('symbols');
var OPSymbols = shared('op-symbols');
var ObjectProto = Object[PROTOTYPE];
var USE_NATIVE = typeof $Symbol == 'function' && !!$GOPS.f;
var QObject = global.QObject;
// Don't use setters in Qt Script, https://github.com/zloirock/core-js/issues/173
var setter = !QObject || !QObject[PROTOTYPE] || !QObject[PROTOTYPE].findChild;

// fallback for old Android, https://code.google.com/p/v8/issues/detail?id=687
var setSymbolDesc = DESCRIPTORS && $fails(function () {
  return _create(dP({}, 'a', {
    get: function () { return dP(this, 'a', { value: 7 }).a; }
  })).a != 7;
}) ? function (it, key, D) {
  var protoDesc = gOPD(ObjectProto, key);
  if (protoDesc) delete ObjectProto[key];
  dP(it, key, D);
  if (protoDesc && it !== ObjectProto) dP(ObjectProto, key, protoDesc);
} : dP;

var wrap = function (tag) {
  var sym = AllSymbols[tag] = _create($Symbol[PROTOTYPE]);
  sym._k = tag;
  return sym;
};

var isSymbol = USE_NATIVE && typeof $Symbol.iterator == 'symbol' ? function (it) {
  return typeof it == 'symbol';
} : function (it) {
  return it instanceof $Symbol;
};

var $defineProperty = function defineProperty(it, key, D) {
  if (it === ObjectProto) $defineProperty(OPSymbols, key, D);
  anObject(it);
  key = toPrimitive(key, true);
  anObject(D);
  if (has(AllSymbols, key)) {
    if (!D.enumerable) {
      if (!has(it, HIDDEN)) dP(it, HIDDEN, createDesc(1, {}));
      it[HIDDEN][key] = true;
    } else {
      if (has(it, HIDDEN) && it[HIDDEN][key]) it[HIDDEN][key] = false;
      D = _create(D, { enumerable: createDesc(0, false) });
    } return setSymbolDesc(it, key, D);
  } return dP(it, key, D);
};
var $defineProperties = function defineProperties(it, P) {
  anObject(it);
  var keys = enumKeys(P = toIObject(P));
  var i = 0;
  var l = keys.length;
  var key;
  while (l > i) $defineProperty(it, key = keys[i++], P[key]);
  return it;
};
var $create = function create(it, P) {
  return P === undefined ? _create(it) : $defineProperties(_create(it), P);
};
var $propertyIsEnumerable = function propertyIsEnumerable(key) {
  var E = isEnum.call(this, key = toPrimitive(key, true));
  if (this === ObjectProto && has(AllSymbols, key) && !has(OPSymbols, key)) return false;
  return E || !has(this, key) || !has(AllSymbols, key) || has(this, HIDDEN) && this[HIDDEN][key] ? E : true;
};
var $getOwnPropertyDescriptor = function getOwnPropertyDescriptor(it, key) {
  it = toIObject(it);
  key = toPrimitive(key, true);
  if (it === ObjectProto && has(AllSymbols, key) && !has(OPSymbols, key)) return;
  var D = gOPD(it, key);
  if (D && has(AllSymbols, key) && !(has(it, HIDDEN) && it[HIDDEN][key])) D.enumerable = true;
  return D;
};
var $getOwnPropertyNames = function getOwnPropertyNames(it) {
  var names = gOPN(toIObject(it));
  var result = [];
  var i = 0;
  var key;
  while (names.length > i) {
    if (!has(AllSymbols, key = names[i++]) && key != HIDDEN && key != META) result.push(key);
  } return result;
};
var $getOwnPropertySymbols = function getOwnPropertySymbols(it) {
  var IS_OP = it === ObjectProto;
  var names = gOPN(IS_OP ? OPSymbols : toIObject(it));
  var result = [];
  var i = 0;
  var key;
  while (names.length > i) {
    if (has(AllSymbols, key = names[i++]) && (IS_OP ? has(ObjectProto, key) : true)) result.push(AllSymbols[key]);
  } return result;
};

// 19.4.1.1 Symbol([description])
if (!USE_NATIVE) {
  $Symbol = function Symbol() {
    if (this instanceof $Symbol) throw TypeError('Symbol is not a constructor!');
    var tag = uid(arguments.length > 0 ? arguments[0] : undefined);
    var $set = function (value) {
      if (this === ObjectProto) $set.call(OPSymbols, value);
      if (has(this, HIDDEN) && has(this[HIDDEN], tag)) this[HIDDEN][tag] = false;
      setSymbolDesc(this, tag, createDesc(1, value));
    };
    if (DESCRIPTORS && setter) setSymbolDesc(ObjectProto, tag, { configurable: true, set: $set });
    return wrap(tag);
  };
  redefine($Symbol[PROTOTYPE], 'toString', function toString() {
    return this._k;
  });

  $GOPD.f = $getOwnPropertyDescriptor;
  $DP.f = $defineProperty;
  __webpack_require__(101).f = gOPNExt.f = $getOwnPropertyNames;
  __webpack_require__(42).f = $propertyIsEnumerable;
  $GOPS.f = $getOwnPropertySymbols;

  if (DESCRIPTORS && !__webpack_require__(21)) {
    redefine(ObjectProto, 'propertyIsEnumerable', $propertyIsEnumerable, true);
  }

  wksExt.f = function (name) {
    return wrap(wks(name));
  };
}

$export($export.G + $export.W + $export.F * !USE_NATIVE, { Symbol: $Symbol });

for (var es6Symbols = (
  // 19.4.2.2, 19.4.2.3, 19.4.2.4, 19.4.2.6, 19.4.2.8, 19.4.2.9, 19.4.2.10, 19.4.2.11, 19.4.2.12, 19.4.2.13, 19.4.2.14
  'hasInstance,isConcatSpreadable,iterator,match,replace,search,species,split,toPrimitive,toStringTag,unscopables'
).split(','), j = 0; es6Symbols.length > j;)wks(es6Symbols[j++]);

for (var wellKnownSymbols = $keys(wks.store), k = 0; wellKnownSymbols.length > k;) wksDefine(wellKnownSymbols[k++]);

$export($export.S + $export.F * !USE_NATIVE, 'Symbol', {
  // 19.4.2.1 Symbol.for(key)
  'for': function (key) {
    return has(SymbolRegistry, key += '')
      ? SymbolRegistry[key]
      : SymbolRegistry[key] = $Symbol(key);
  },
  // 19.4.2.5 Symbol.keyFor(sym)
  keyFor: function keyFor(sym) {
    if (!isSymbol(sym)) throw TypeError(sym + ' is not a symbol!');
    for (var key in SymbolRegistry) if (SymbolRegistry[key] === sym) return key;
  },
  useSetter: function () { setter = true; },
  useSimple: function () { setter = false; }
});

$export($export.S + $export.F * !USE_NATIVE, 'Object', {
  // 19.1.2.2 Object.create(O [, Properties])
  create: $create,
  // 19.1.2.4 Object.defineProperty(O, P, Attributes)
  defineProperty: $defineProperty,
  // 19.1.2.3 Object.defineProperties(O, Properties)
  defineProperties: $defineProperties,
  // 19.1.2.6 Object.getOwnPropertyDescriptor(O, P)
  getOwnPropertyDescriptor: $getOwnPropertyDescriptor,
  // 19.1.2.7 Object.getOwnPropertyNames(O)
  getOwnPropertyNames: $getOwnPropertyNames,
  // 19.1.2.8 Object.getOwnPropertySymbols(O)
  getOwnPropertySymbols: $getOwnPropertySymbols
});

// Chrome 38 and 39 `Object.getOwnPropertySymbols` fails on primitives
// https://bugs.chromium.org/p/v8/issues/detail?id=3443
var FAILS_ON_PRIMITIVES = $fails(function () { $GOPS.f(1); });

$export($export.S + $export.F * FAILS_ON_PRIMITIVES, 'Object', {
  getOwnPropertySymbols: function getOwnPropertySymbols(it) {
    return $GOPS.f(toObject(it));
  }
});

// 24.3.2 JSON.stringify(value [, replacer [, space]])
$JSON && $export($export.S + $export.F * (!USE_NATIVE || $fails(function () {
  var S = $Symbol();
  // MS Edge converts symbol values to JSON as {}
  // WebKit converts symbol values to JSON as null
  // V8 throws on boxed symbols
  return _stringify([S]) != '[null]' || _stringify({ a: S }) != '{}' || _stringify(Object(S)) != '{}';
})), 'JSON', {
  stringify: function stringify(it) {
    var args = [it];
    var i = 1;
    var replacer, $replacer;
    while (arguments.length > i) args.push(arguments[i++]);
    $replacer = replacer = args[1];
    if (!isObject(replacer) && it === undefined || isSymbol(it)) return; // IE8 returns string on undefined
    if (!isArray(replacer)) replacer = function (key, value) {
      if (typeof $replacer == 'function') value = $replacer.call(this, key, value);
      if (!isSymbol(value)) return value;
    };
    args[1] = replacer;
    return _stringify.apply($JSON, args);
  }
});

// 19.4.3.4 Symbol.prototype[@@toPrimitive](hint)
$Symbol[PROTOTYPE][TO_PRIMITIVE] || __webpack_require__(13)($Symbol[PROTOTYPE], TO_PRIMITIVE, $Symbol[PROTOTYPE].valueOf);
// 19.4.3.5 Symbol.prototype[@@toStringTag]
setToStringTag($Symbol, 'Symbol');
// 20.2.1.9 Math[@@toStringTag]
setToStringTag(Math, 'Math', true);
// 24.3.3 JSON[@@toStringTag]
setToStringTag(global.JSON, 'JSON', true);


/***/ }),
/* 149 */
/***/ (function(module, exports, __webpack_require__) {

// all enumerable object keys, includes symbols
var getKeys = __webpack_require__(26);
var gOPS = __webpack_require__(95);
var pIE = __webpack_require__(42);
module.exports = function (it) {
  var result = getKeys(it);
  var getSymbols = gOPS.f;
  if (getSymbols) {
    var symbols = getSymbols(it);
    var isEnum = pIE.f;
    var i = 0;
    var key;
    while (symbols.length > i) if (isEnum.call(it, key = symbols[i++])) result.push(key);
  } return result;
};


/***/ }),
/* 150 */
/***/ (function(module, exports, __webpack_require__) {

var $export = __webpack_require__(2);
// 19.1.2.2 / 15.2.3.5 Object.create(O [, Properties])
$export($export.S, 'Object', { create: __webpack_require__(48) });


/***/ }),
/* 151 */
/***/ (function(module, exports, __webpack_require__) {

var $export = __webpack_require__(2);
// 19.1.2.4 / 15.2.3.6 Object.defineProperty(O, P, Attributes)
$export($export.S + $export.F * !__webpack_require__(5), 'Object', { defineProperty: __webpack_require__(10).f });


/***/ }),
/* 152 */
/***/ (function(module, exports, __webpack_require__) {

var $export = __webpack_require__(2);
// 19.1.2.3 / 15.2.3.7 Object.defineProperties(O, Properties)
$export($export.S + $export.F * !__webpack_require__(5), 'Object', { defineProperties: __webpack_require__(60) });


/***/ }),
/* 153 */
/***/ (function(module, exports, __webpack_require__) {

// 19.1.2.6 Object.getOwnPropertyDescriptor(O, P)
var toIObject = __webpack_require__(14);
var $getOwnPropertyDescriptor = __webpack_require__(28).f;

__webpack_require__(36)('getOwnPropertyDescriptor', function () {
  return function getOwnPropertyDescriptor(it, key) {
    return $getOwnPropertyDescriptor(toIObject(it), key);
  };
});


/***/ }),
/* 154 */
/***/ (function(module, exports, __webpack_require__) {

// 19.1.2.9 Object.getPrototypeOf(O)
var toObject = __webpack_require__(9);
var $getPrototypeOf = __webpack_require__(35);

__webpack_require__(36)('getPrototypeOf', function () {
  return function getPrototypeOf(it) {
    return $getPrototypeOf(toObject(it));
  };
});


/***/ }),
/* 155 */
/***/ (function(module, exports, __webpack_require__) {

// 19.1.2.14 Object.keys(O)
var toObject = __webpack_require__(9);
var $keys = __webpack_require__(26);

__webpack_require__(36)('keys', function () {
  return function keys(it) {
    return $keys(toObject(it));
  };
});


/***/ }),
/* 156 */
/***/ (function(module, exports, __webpack_require__) {

// 19.1.2.7 Object.getOwnPropertyNames(O)
__webpack_require__(36)('getOwnPropertyNames', function () {
  return __webpack_require__(110).f;
});


/***/ }),
/* 157 */
/***/ (function(module, exports, __webpack_require__) {

// 19.1.2.5 Object.freeze(O)
var isObject = __webpack_require__(8);
var meta = __webpack_require__(94).onFreeze;

__webpack_require__(36)('freeze', function ($freeze) {
  return function freeze(it) {
    return $freeze && isObject(it) ? $freeze(meta(it)) : it;
  };
});


/***/ }),
/* 158 */
/***/ (function(module, exports, __webpack_require__) {

// 19.1.2.17 Object.seal(O)
var isObject = __webpack_require__(8);
var meta = __webpack_require__(94).onFreeze;

__webpack_require__(36)('seal', function ($seal) {
  return function seal(it) {
    return $seal && isObject(it) ? $seal(meta(it)) : it;
  };
});


/***/ }),
/* 159 */
/***/ (function(module, exports, __webpack_require__) {

// 19.1.2.15 Object.preventExtensions(O)
var isObject = __webpack_require__(8);
var meta = __webpack_require__(94).onFreeze;

__webpack_require__(36)('preventExtensions', function ($preventExtensions) {
  return function preventExtensions(it) {
    return $preventExtensions && isObject(it) ? $preventExtensions(meta(it)) : it;
  };
});


/***/ }),
/* 160 */
/***/ (function(module, exports, __webpack_require__) {

// 19.1.2.12 Object.isFrozen(O)
var isObject = __webpack_require__(8);

__webpack_require__(36)('isFrozen', function ($isFrozen) {
  return function isFrozen(it) {
    return isObject(it) ? $isFrozen ? $isFrozen(it) : false : true;
  };
});


/***/ }),
/* 161 */
/***/ (function(module, exports, __webpack_require__) {

// 19.1.2.13 Object.isSealed(O)
var isObject = __webpack_require__(8);

__webpack_require__(36)('isSealed', function ($isSealed) {
  return function isSealed(it) {
    return isObject(it) ? $isSealed ? $isSealed(it) : false : true;
  };
});


/***/ }),
/* 162 */
/***/ (function(module, exports, __webpack_require__) {

// 19.1.2.11 Object.isExtensible(O)
var isObject = __webpack_require__(8);

__webpack_require__(36)('isExtensible', function ($isExtensible) {
  return function isExtensible(it) {
    return isObject(it) ? $isExtensible ? $isExtensible(it) : true : false;
  };
});


/***/ }),
/* 163 */
/***/ (function(module, exports, __webpack_require__) {

// 19.1.3.1 Object.assign(target, source)
var $export = __webpack_require__(2);

$export($export.S + $export.F, 'Object', { assign: __webpack_require__(164) });


/***/ }),
/* 164 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

// 19.1.2.1 Object.assign(target, source, ...)
var DESCRIPTORS = __webpack_require__(5);
var getKeys = __webpack_require__(26);
var gOPS = __webpack_require__(95);
var pIE = __webpack_require__(42);
var toObject = __webpack_require__(9);
var IObject = __webpack_require__(59);
var $assign = Object.assign;

// should work with symbols and should have deterministic property order (V8 bug)
module.exports = !$assign || __webpack_require__(11)(function () {
  var A = {};
  var B = {};
  // eslint-disable-next-line no-undef
  var S = Symbol();
  var K = 'abcdefghijklmnopqrst';
  A[S] = 7;
  K.split('').forEach(function (k) { B[k] = k; });
  return $assign({}, A)[S] != 7 || Object.keys($assign({}, B)).join('') != K;
}) ? function assign(target, source) { // eslint-disable-line no-unused-vars
  var T = toObject(target);
  var aLen = arguments.length;
  var index = 1;
  var getSymbols = gOPS.f;
  var isEnum = pIE.f;
  while (aLen > index) {
    var S = IObject(arguments[index++]);
    var keys = getSymbols ? getKeys(S).concat(getSymbols(S)) : getKeys(S);
    var length = keys.length;
    var j = 0;
    var key;
    while (length > j) {
      key = keys[j++];
      if (!DESCRIPTORS || isEnum.call(S, key)) T[key] = S[key];
    }
  } return T;
} : $assign;


/***/ }),
/* 165 */
/***/ (function(module, exports, __webpack_require__) {

// 19.1.3.10 Object.is(value1, value2)
var $export = __webpack_require__(2);
$export($export.S, 'Object', { is: __webpack_require__(166) });


/***/ }),
/* 166 */
/***/ (function(module, exports) {

// 7.2.9 SameValue(x, y)
module.exports = Object.is || function is(x, y) {
  // eslint-disable-next-line no-self-compare
  return x === y ? x !== 0 || 1 / x === 1 / y : x != x && y != y;
};


/***/ }),
/* 167 */
/***/ (function(module, exports, __webpack_require__) {

// 19.1.3.19 Object.setPrototypeOf(O, proto)
var $export = __webpack_require__(2);
$export($export.S, 'Object', { setPrototypeOf: __webpack_require__(168).set });


/***/ }),
/* 168 */
/***/ (function(module, exports, __webpack_require__) {

// Works with __proto__ only. Old v8 can't work with null proto objects.
/* eslint-disable no-proto */
var isObject = __webpack_require__(8);
var anObject = __webpack_require__(17);
var check = function (O, proto) {
  anObject(O);
  if (!isObject(proto) && proto !== null) throw TypeError(proto + ": can't set as prototype!");
};
module.exports = {
  set: Object.setPrototypeOf || ('__proto__' in {} ? // eslint-disable-line
    function (test, buggy, set) {
      try {
        set = __webpack_require__(33)(Function.call, __webpack_require__(28).f(Object.prototype, '__proto__').set, 2);
        set(test, []);
        buggy = !(test instanceof Array);
      } catch (e) { buggy = true; }
      return function setPrototypeOf(O, proto) {
        check(O, proto);
        if (buggy) O.__proto__ = proto;
        else set(O, proto);
        return O;
      };
    }({}, false) : undefined),
  check: check
};


/***/ }),
/* 169 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

// 19.1.3.6 Object.prototype.toString()
var classof = __webpack_require__(111);
var test = {};
test[__webpack_require__(6)('toStringTag')] = 'z';
if (test + '' != '[object z]') {
  __webpack_require__(30)(Object.prototype, 'toString', function toString() {
    return '[object ' + classof(this) + ']';
  }, true);
}


/***/ }),
/* 170 */
/***/ (function(module, exports, __webpack_require__) {

// https://github.com/tc39/proposal-object-getownpropertydescriptors
var $export = __webpack_require__(2);
var ownKeys = __webpack_require__(112);
var toIObject = __webpack_require__(14);
var gOPD = __webpack_require__(28);
var createProperty = __webpack_require__(171);

$export($export.S, 'Object', {
  getOwnPropertyDescriptors: function getOwnPropertyDescriptors(object) {
    var O = toIObject(object);
    var getDesc = gOPD.f;
    var keys = ownKeys(O);
    var result = {};
    var i = 0;
    var key, desc;
    while (keys.length > i) {
      desc = getDesc(O, key = keys[i++]);
      if (desc !== undefined) createProperty(result, key, desc);
    }
    return result;
  }
});


/***/ }),
/* 171 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var $defineProperty = __webpack_require__(10);
var createDesc = __webpack_require__(29);

module.exports = function (object, index, value) {
  if (index in object) $defineProperty.f(object, index, createDesc(0, value));
  else object[index] = value;
};


/***/ }),
/* 172 */
/***/ (function(module, exports, __webpack_require__) {

// https://github.com/tc39/proposal-object-values-entries
var $export = __webpack_require__(2);
var $values = __webpack_require__(113)(false);

$export($export.S, 'Object', {
  values: function values(it) {
    return $values(it);
  }
});


/***/ }),
/* 173 */
/***/ (function(module, exports, __webpack_require__) {

// https://github.com/tc39/proposal-object-values-entries
var $export = __webpack_require__(2);
var $entries = __webpack_require__(113)(true);

$export($export.S, 'Object', {
  entries: function entries(it) {
    return $entries(it);
  }
});


/***/ }),
/* 174 */
/***/ (function(module, exports, __webpack_require__) {

var $export = __webpack_require__(2);

$export($export.S + $export.F, 'Object', { isObject: __webpack_require__(8) });


/***/ }),
/* 175 */
/***/ (function(module, exports, __webpack_require__) {

var $export = __webpack_require__(2);

$export($export.S + $export.F, 'Object', { classof: __webpack_require__(111) });


/***/ }),
/* 176 */
/***/ (function(module, exports, __webpack_require__) {

var $export = __webpack_require__(2);
var define = __webpack_require__(114);

$export($export.S + $export.F, 'Object', { define: define });


/***/ }),
/* 177 */
/***/ (function(module, exports, __webpack_require__) {

var $export = __webpack_require__(2);
var define = __webpack_require__(114);
var create = __webpack_require__(48);

$export($export.S + $export.F, 'Object', {
  make: function (proto, mixin) {
    return define(create(proto), mixin);
  }
});


/***/ }),
/* 178 */
/***/ (function(module, exports) {

exports.endianness = function () { return 'LE' };

exports.hostname = function () {
    if (typeof location !== 'undefined') {
        return location.hostname
    }
    else return '';
};

exports.loadavg = function () { return [] };

exports.uptime = function () { return 0 };

exports.freemem = function () {
    return Number.MAX_VALUE;
};

exports.totalmem = function () {
    return Number.MAX_VALUE;
};

exports.cpus = function () { return [] };

exports.type = function () { return 'Browser' };

exports.release = function () {
    if (typeof navigator !== 'undefined') {
        return navigator.appVersion;
    }
    return '';
};

exports.networkInterfaces
= exports.getNetworkInterfaces
= function () { return {} };

exports.arch = function () { return 'javascript' };

exports.platform = function () { return 'browser' };

exports.tmpdir = exports.tmpDir = function () {
    return '/tmp';
};

exports.EOL = '\n';

exports.homedir = function () {
	return '/'
};


/***/ }),
/* 179 */
/***/ (function(module, exports) {

// shim for using process in browser
var process = module.exports = {};

// cached from whatever global is present so that test runners that stub it
// don't break things.  But we need to wrap it in a try catch in case it is
// wrapped in strict mode code which doesn't define any globals.  It's inside a
// function because try/catches deoptimize in certain engines.

var cachedSetTimeout;
var cachedClearTimeout;

function defaultSetTimout() {
    throw new Error('setTimeout has not been defined');
}
function defaultClearTimeout () {
    throw new Error('clearTimeout has not been defined');
}
(function () {
    try {
        if (typeof setTimeout === 'function') {
            cachedSetTimeout = setTimeout;
        } else {
            cachedSetTimeout = defaultSetTimout;
        }
    } catch (e) {
        cachedSetTimeout = defaultSetTimout;
    }
    try {
        if (typeof clearTimeout === 'function') {
            cachedClearTimeout = clearTimeout;
        } else {
            cachedClearTimeout = defaultClearTimeout;
        }
    } catch (e) {
        cachedClearTimeout = defaultClearTimeout;
    }
} ())
function runTimeout(fun) {
    if (cachedSetTimeout === setTimeout) {
        //normal enviroments in sane situations
        return setTimeout(fun, 0);
    }
    // if setTimeout wasn't available but was latter defined
    if ((cachedSetTimeout === defaultSetTimout || !cachedSetTimeout) && setTimeout) {
        cachedSetTimeout = setTimeout;
        return setTimeout(fun, 0);
    }
    try {
        // when when somebody has screwed with setTimeout but no I.E. maddness
        return cachedSetTimeout(fun, 0);
    } catch(e){
        try {
            // When we are in I.E. but the script has been evaled so I.E. doesn't trust the global object when called normally
            return cachedSetTimeout.call(null, fun, 0);
        } catch(e){
            // same as above but when it's a version of I.E. that must have the global object for 'this', hopfully our context correct otherwise it will throw a global error
            return cachedSetTimeout.call(this, fun, 0);
        }
    }


}
function runClearTimeout(marker) {
    if (cachedClearTimeout === clearTimeout) {
        //normal enviroments in sane situations
        return clearTimeout(marker);
    }
    // if clearTimeout wasn't available but was latter defined
    if ((cachedClearTimeout === defaultClearTimeout || !cachedClearTimeout) && clearTimeout) {
        cachedClearTimeout = clearTimeout;
        return clearTimeout(marker);
    }
    try {
        // when when somebody has screwed with setTimeout but no I.E. maddness
        return cachedClearTimeout(marker);
    } catch (e){
        try {
            // When we are in I.E. but the script has been evaled so I.E. doesn't  trust the global object when called normally
            return cachedClearTimeout.call(null, marker);
        } catch (e){
            // same as above but when it's a version of I.E. that must have the global object for 'this', hopfully our context correct otherwise it will throw a global error.
            // Some versions of I.E. have different rules for clearTimeout vs setTimeout
            return cachedClearTimeout.call(this, marker);
        }
    }



}
var queue = [];
var draining = false;
var currentQueue;
var queueIndex = -1;

function cleanUpNextTick() {
    if (!draining || !currentQueue) {
        return;
    }
    draining = false;
    if (currentQueue.length) {
        queue = currentQueue.concat(queue);
    } else {
        queueIndex = -1;
    }
    if (queue.length) {
        drainQueue();
    }
}

function drainQueue() {
    if (draining) {
        return;
    }
    var timeout = runTimeout(cleanUpNextTick);
    draining = true;

    var len = queue.length;
    while(len) {
        currentQueue = queue;
        queue = [];
        while (++queueIndex < len) {
            if (currentQueue) {
                currentQueue[queueIndex].run();
            }
        }
        queueIndex = -1;
        len = queue.length;
    }
    currentQueue = null;
    draining = false;
    runClearTimeout(timeout);
}

process.nextTick = function (fun) {
    var args = new Array(arguments.length - 1);
    if (arguments.length > 1) {
        for (var i = 1; i < arguments.length; i++) {
            args[i - 1] = arguments[i];
        }
    }
    queue.push(new Item(fun, args));
    if (queue.length === 1 && !draining) {
        runTimeout(drainQueue);
    }
};

// v8 likes predictible objects
function Item(fun, array) {
    this.fun = fun;
    this.array = array;
}
Item.prototype.run = function () {
    this.fun.apply(null, this.array);
};
process.title = 'browser';
process.browser = true;
process.env = {};
process.argv = [];
process.version = ''; // empty string to avoid regexp issues
process.versions = {};

function noop() {}

process.on = noop;
process.addListener = noop;
process.once = noop;
process.off = noop;
process.removeListener = noop;
process.removeAllListeners = noop;
process.emit = noop;
process.prependListener = noop;
process.prependOnceListener = noop;

process.listeners = function (name) { return [] }

process.binding = function (name) {
    throw new Error('process.binding is not supported');
};

process.cwd = function () { return '/' };
process.chdir = function (dir) {
    throw new Error('process.chdir is not supported');
};
process.umask = function() { return 0; };


/***/ }),
/* 180 */
/***/ (function(module) {

module.exports = JSON.parse("[{\"name\":\"CA Toronto\",\"iso\":\"CA\",\"dns\":\"ca-toronto.http-proxy.privateinternetbrowsing.com\",\"ping\":\"66.115.142.129\",\"port\":443,\"mace\":80},{\"name\":\"CA Montreal\",\"iso\":\"CA\",\"dns\":\"ca-montreal.http-proxy.privateinternetbrowsing.com\",\"ping\":\"172.98.71.126\",\"port\":443,\"mace\":80},{\"name\":\"JP Tokyo\",\"iso\":\"JP\",\"dns\":\"japan.http-proxy.privateinternetbrowsing.com\",\"ping\":\"156.146.34.33\",\"port\":443,\"mace\":80},{\"name\":\"BE Brussels\",\"iso\":\"BE\",\"dns\":\"brussels.http-proxy.privateinternetbrowsing.com\",\"ping\":\"91.207.57.44\",\"port\":443,\"mace\":80},{\"name\":\"DE Frankfurt\",\"iso\":\"DE\",\"dns\":\"de-frankfurt.http-proxy.privateinternetbrowsing.com\",\"ping\":\"82.102.16.13\",\"port\":443,\"mace\":80},{\"name\":\"DE Berlin\",\"iso\":\"DE\",\"dns\":\"de-berlin.http-proxy.privateinternetbrowsing.com\",\"ping\":\"37.120.217.27\",\"port\":443,\"mace\":80},{\"name\":\"HU Budapest\",\"iso\":\"HU\",\"dns\":\"hungary.http-proxy.privateinternetbrowsing.com\",\"ping\":\"185.252.223.146\",\"port\":443,\"mace\":80},{\"name\":\"US Silicon Valley\",\"iso\":\"US\",\"dns\":\"us-siliconvalley.http-proxy.privateinternetbrowsing.com\",\"ping\":\"66.115.165.63\",\"port\":443,\"mace\":80},{\"name\":\"US Washington DC\",\"iso\":\"US\",\"dns\":\"us-washingtondc.http-proxy.privateinternetbrowsing.com\",\"ping\":\"70.32.1.86\",\"port\":443,\"mace\":80},{\"name\":\"UK Manchester\",\"iso\":\"UK\",\"dns\":\"uk-manchester.http-proxy.privateinternetbrowsing.com\",\"ping\":\"89.249.74.173\",\"port\":443,\"mace\":80},{\"name\":\"UK London\",\"iso\":\"UK\",\"dns\":\"uk-london.http-proxy.privateinternetbrowsing.com\",\"ping\":\"212.102.53.138\",\"port\":443,\"mace\":80},{\"name\":\"PL Warsaw\",\"iso\":\"PL\",\"dns\":\"poland.http-proxy.privateinternetbrowsing.com\",\"ping\":\"138.199.59.231\",\"port\":443,\"mace\":80},{\"name\":\"US Los Angeles\",\"iso\":\"US\",\"dns\":\"us-california.http-proxy.privateinternetbrowsing.com\",\"ping\":\"146.70.49.198\",\"port\":443,\"mace\":80},{\"name\":\"US Las Vegas\",\"iso\":\"US\",\"dns\":\"us-lasvegas.http-proxy.privateinternetbrowsing.com\",\"ping\":\"45.89.173.242\",\"port\":443,\"mace\":80},{\"name\":\"FR Paris\",\"iso\":\"FR\",\"dns\":\"france.http-proxy.privateinternetbrowsing.com\",\"ping\":\"146.70.40.203\",\"port\":443,\"mace\":80},{\"name\":\"RO Bucharest\",\"iso\":\"RO\",\"dns\":\"ro.http-proxy.privateinternetbrowsing.com\",\"ping\":\"143.244.54.37\",\"port\":443,\"mace\":80},{\"name\":\"AE Abu Dhabi\",\"iso\":\"AE\",\"dns\":\"ae.http-proxy.privateinternetbrowsing.com\",\"ping\":\"146.70.37.130\",\"port\":443,\"mace\":80},{\"name\":\"US Seattle\",\"iso\":\"US\",\"dns\":\"us-seattle.http-proxy.privateinternetbrowsing.com\",\"ping\":\"156.146.49.2\",\"port\":443,\"mace\":80},{\"name\":\"US Phoenix\",\"iso\":\"US\",\"dns\":\"us3.http-proxy.privateinternetbrowsing.com\",\"ping\":\"107.181.185.114\",\"port\":443,\"mace\":80},{\"name\":\"LU Luxembourg\",\"iso\":\"LU\",\"dns\":\"lu.http-proxy.privateinternetbrowsing.com\",\"ping\":\"5.253.204.156\",\"port\":443,\"mace\":80},{\"name\":\"SE Stockholm\",\"iso\":\"SE\",\"dns\":\"sweden.http-proxy.privateinternetbrowsing.com\",\"ping\":\"146.70.21.93\",\"port\":443,\"mace\":80},{\"name\":\"AU Melbourne\",\"iso\":\"AU\",\"dns\":\"aus-melbourne.http-proxy.privateinternetbrowsing.com\",\"ping\":\"221.121.139.162\",\"port\":443,\"mace\":80},{\"name\":\"NO Oslo\",\"iso\":\"NO\",\"dns\":\"no.http-proxy.privateinternetbrowsing.com\",\"ping\":\"146.70.17.44\",\"port\":443,\"mace\":80},{\"name\":\"US Atlanta\",\"iso\":\"US\",\"dns\":\"us-atlanta.http-proxy.privateinternetbrowsing.com\",\"ping\":\"156.146.47.9\",\"port\":443,\"mace\":80},{\"name\":\"US Dallas\",\"iso\":\"US\",\"dns\":\"us-texas.http-proxy.privateinternetbrowsing.com\",\"ping\":\"156.146.39.79\",\"port\":443,\"mace\":80},{\"name\":\"DK Copenhagen\",\"iso\":\"DK\",\"dns\":\"denmark.http-proxy.privateinternetbrowsing.com\",\"ping\":\"146.70.42.125\",\"port\":443,\"mace\":80},{\"name\":\"US Chicago\",\"iso\":\"US\",\"dns\":\"us-chicago.http-proxy.privateinternetbrowsing.com\",\"ping\":\"143.244.60.147\",\"port\":443,\"mace\":80},{\"name\":\"US Denver\",\"iso\":\"US\",\"dns\":\"us-denver.http-proxy.privateinternetbrowsing.com\",\"ping\":\"199.115.96.75\",\"port\":443,\"mace\":80},{\"name\":\"US Miami\",\"iso\":\"US\",\"dns\":\"us-florida.http-proxy.privateinternetbrowsing.com\",\"ping\":\"37.120.157.149\",\"port\":443,\"mace\":80},{\"name\":\"CZ Prague\",\"iso\":\"CZ\",\"dns\":\"czech.http-proxy.privateinternetbrowsing.com\",\"ping\":\"212.102.39.162\",\"port\":443,\"mace\":80},{\"name\":\"ES Madrid\",\"iso\":\"ES\",\"dns\":\"spain.http-proxy.privateinternetbrowsing.com\",\"ping\":\"45.128.39.242\",\"port\":443,\"mace\":80},{\"name\":\"US Houston\",\"iso\":\"US\",\"dns\":\"us-houston.http-proxy.privateinternetbrowsing.com\",\"ping\":\"156.146.39.218\",\"port\":443,\"mace\":80},{\"name\":\"US New York\",\"iso\":\"US\",\"dns\":\"us-newyorkcity.http-proxy.privateinternetbrowsing.com\",\"ping\":\"138.199.13.168\",\"port\":443,\"mace\":80},{\"name\":\"AU Sydney\",\"iso\":\"AU\",\"dns\":\"au-sydney.http-proxy.privateinternetbrowsing.com\",\"ping\":\"27.50.87.163\",\"port\":443,\"mace\":80},{\"name\":\"NZ Wellington\",\"iso\":\"NZ\",\"dns\":\"nz.http-proxy.privateinternetbrowsing.com\",\"ping\":\"221.121.135.163\",\"port\":443,\"mace\":80},{\"name\":\"NL Amsterdam\",\"iso\":\"NL\",\"dns\":\"nl-amsterdam.http-proxy.privateinternetbrowsing.com\",\"ping\":\"109.201.152.187\",\"port\":443,\"mace\":80},{\"name\":\"FI Helsinki\",\"iso\":\"FI\",\"dns\":\"fi.http-proxy.privateinternetbrowsing.com\",\"ping\":\"46.246.34.27\",\"port\":443,\"mace\":80},{\"name\":\"AT Vienna\",\"iso\":\"AT\",\"dns\":\"austria.http-proxy.privateinternetbrowsing.com\",\"ping\":\"146.70.28.165\",\"port\":443,\"mace\":80},{\"name\":\"IN Mumbai\",\"iso\":\"IN\",\"dns\":\"in.http-proxy.privateinternetbrowsing.com\",\"ping\":\"45.120.139.101\",\"port\":443,\"mace\":80},{\"name\":\"CA Vancouver\",\"iso\":\"CA\",\"dns\":\"ca-vancouver.http-proxy.privateinternetbrowsing.com\",\"ping\":\"104.200.150.140\",\"port\":443,\"mace\":80},{\"name\":\"US Trenton\",\"iso\":\"US\",\"dns\":\"us-newjersey.http-proxy.privateinternetbrowsing.com\",\"ping\":\"37.120.202.109\",\"port\":443,\"mace\":80},{\"name\":\"IE Dublin\",\"iso\":\"IE\",\"dns\":\"ireland.http-proxy.privateinternetbrowsing.com\",\"ping\":\"146.70.48.234\",\"port\":443,\"mace\":80},{\"name\":\"UK Southampton\",\"iso\":\"UK\",\"dns\":\"uk-southampton.http-proxy.privateinternetbrowsing.com\",\"ping\":\"138.199.28.159\",\"port\":443,\"mace\":80},{\"name\":\"IT Milano\",\"iso\":\"IT\",\"dns\":\"italy.http-proxy.privateinternetbrowsing.com\",\"ping\":\"217.138.197.229\",\"port\":443,\"mace\":80},{\"name\":\"SG Singapore\",\"iso\":\"SG\",\"dns\":\"sg.http-proxy.privateinternetbrowsing.com\",\"ping\":\"156.146.57.6\",\"port\":443,\"mace\":80},{\"name\":\"IL Jerusalem\",\"iso\":\"IL\",\"dns\":\"israel.http-proxy.privateinternetbrowsing.com\",\"ping\":\"185.191.205.67\",\"port\":443,\"mace\":80}]");

/***/ }),
/* 181 */,
/* 182 */,
/* 183 */,
/* 184 */,
/* 185 */,
/* 186 */,
/* 187 */,
/* 188 */,
/* 189 */,
/* 190 */,
/* 191 */,
/* 192 */,
/* 193 */,
/* 194 */,
/* 195 */,
/* 196 */,
/* 197 */,
/* 198 */,
/* 199 */,
/* 200 */,
/* 201 */,
/* 202 */,
/* 203 */,
/* 204 */,
/* 205 */,
/* 206 */,
/* 207 */,
/* 208 */,
/* 209 */,
/* 210 */,
/* 211 */,
/* 212 */,
/* 213 */,
/* 214 */,
/* 215 */,
/* 216 */,
/* 217 */,
/* 218 */,
/* 219 */,
/* 220 */,
/* 221 */,
/* 222 */,
/* 223 */,
/* 224 */,
/* 225 */,
/* 226 */,
/* 227 */,
/* 228 */,
/* 229 */,
/* 230 */,
/* 231 */,
/* 232 */,
/* 233 */,
/* 234 */,
/* 235 */,
/* 236 */,
/* 237 */,
/* 238 */,
/* 239 */,
/* 240 */
/***/ (function(module, exports, __webpack_require__) {

module.exports = __webpack_require__(265);


/***/ }),
/* 241 */,
/* 242 */,
/* 243 */,
/* 244 */,
/* 245 */,
/* 246 */,
/* 247 */,
/* 248 */,
/* 249 */,
/* 250 */,
/* 251 */,
/* 252 */,
/* 253 */,
/* 254 */,
/* 255 */,
/* 256 */,
/* 257 */,
/* 258 */,
/* 259 */,
/* 260 */,
/* 261 */,
/* 262 */,
/* 263 */,
/* 264 */,
/* 265 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// EXTERNAL MODULE: ./node_modules/core-js/modules/es7.array.flat-map.js
var es7_array_flat_map = __webpack_require__(66);

// EXTERNAL MODULE: ./node_modules/core-js/modules/es6.array.iterator.js
var es6_array_iterator = __webpack_require__(47);

// EXTERNAL MODULE: ./node_modules/core-js/modules/es6.array.sort.js
var es6_array_sort = __webpack_require__(67);

// EXTERNAL MODULE: ./node_modules/core-js/modules/es7.object.define-getter.js
var es7_object_define_getter = __webpack_require__(55);

// EXTERNAL MODULE: ./node_modules/core-js/modules/es7.object.define-setter.js
var es7_object_define_setter = __webpack_require__(56);

// EXTERNAL MODULE: ./node_modules/core-js/modules/es7.object.lookup-getter.js
var es7_object_lookup_getter = __webpack_require__(57);

// EXTERNAL MODULE: ./node_modules/core-js/modules/es7.object.lookup-setter.js
var es7_object_lookup_setter = __webpack_require__(58);

// EXTERNAL MODULE: ./node_modules/core-js/modules/es7.promise.finally.js
var es7_promise_finally = __webpack_require__(68);

// EXTERNAL MODULE: ./node_modules/core-js/modules/es7.symbol.async-iterator.js
var es7_symbol_async_iterator = __webpack_require__(69);

// EXTERNAL MODULE: ./node_modules/core-js/modules/es7.string.trim-left.js
var es7_string_trim_left = __webpack_require__(70);

// EXTERNAL MODULE: ./node_modules/core-js/modules/es7.string.trim-right.js
var es7_string_trim_right = __webpack_require__(71);

// EXTERNAL MODULE: ./node_modules/core-js/modules/web.timers.js
var web_timers = __webpack_require__(72);

// EXTERNAL MODULE: ./node_modules/core-js/modules/web.immediate.js
var web_immediate = __webpack_require__(73);

// EXTERNAL MODULE: ./node_modules/core-js/modules/web.dom.iterable.js
var web_dom_iterable = __webpack_require__(74);

// EXTERNAL MODULE: ./src/js/sameApp.js
var js_sameApp = __webpack_require__(115);

// EXTERNAL MODULE: ./src/js/helpers/isDev.js
var isDev = __webpack_require__(102);

// CONCATENATED MODULE: ./src/js/util/storage.js


function getLegacyInfo() {
  return [{
    key: 'app::justInTimeDismissed',
    type: 'bool'
  }, {
    key: 'form:password',
    type: 'string'
  }, {
    key: 'sameAppBrowser',
    type: 'string'
  }, {
    key: 'form:username',
    type: 'string'
  }, {
    key: 'showFavorites',
    type: 'bool'
  }, {
    key: 'connectionIndex',
    type: 'number'
  }, {
    key: 'sortby',
    type: 'string'
  }, {
    key: 'visibleISOs',
    type: 'object'
  }, {
    key: 'favoriteregions',
    type: 'string'
  }, {
    key: 'locale',
    type: 'string'
  }, {
    key: 'account',
    type: 'object'
  }, {
    key: 'authToken',
    type: 'string'
  }, {
    key: 'autoRegion',
    type: 'bool'
  }, {
    key: 'bypasslist:customlist',
    type: 'string'
  }, {
    key: 'bypasslist:popularrules',
    type: 'string'
  }, {
    key: 'drawerState',
    type: 'string'
  }, {
    key: 'https-upgrade::last-timestamp',
    type: 'number'
  }, {
    key: 'https-upgrade::last-updated',
    type: 'number'
  }, {
    key: 'https-upgrade::storage-count',
    type: 'number'
  }, {
    key: 'loggedIn',
    type: 'bool'
  }, {
    key: 'online',
    type: 'bool'
  }, {
    key: 'region',
    type: 'object'
  }, {
    key: 'checkSmartLocation',
    type: 'bool'
  }, {
    key: 'smartLocationRules',
    type: 'object'
  }, {
    key: 'regionlist::override',
    type: 'object'
  }, {
    key: 'settings:allowExtensionNotifications',
    type: 'bool'
  }, // { key: 'settings:blockadobeflash', type: 'bool' },
  {
    key: 'settings:blockautofill',
    type: 'bool'
  }, {
    key: 'settings:blockautofilladdress',
    type: 'bool'
  }, {
    key: 'settings:blockautofillcreditcard',
    type: 'bool'
  }, {
    key: 'settings:blockcamera',
    type: 'bool'
  }, {
    key: 'settings:blockfbclid',
    type: 'bool'
  }, {
    key: 'settings:blockhyperlinkaudit',
    type: 'bool'
  }, {
    key: 'settings:blocklocation',
    type: 'bool'
  }, {
    key: 'settings:blockmicrophone',
    type: 'bool'
  }, {
    key: 'settings:blocknetworkprediction',
    type: 'bool'
  }, {
    key: 'settings:blockplugins',
    type: 'bool'
  }, {
    key: 'settings:blockreferer',
    type: 'bool'
  }, {
    key: 'settings:blocksafebrowsing',
    type: 'bool'
  }, {
    key: 'settings:blockthirdpartycookies',
    type: 'bool'
  }, {
    key: 'settings:trackingprotection',
    type: 'bool'
  }, {
    key: 'settings:fingerprintprotection',
    type: 'bool'
  }, {
    key: 'settings:blockutm',
    type: 'bool'
  }, {
    key: 'settings:darkTheme',
    type: 'bool'
  }, {
    key: 'settings:debugmode',
    type: 'bool'
  }, {
    key: 'settings:httpsUpgrade',
    type: 'bool'
  }, {
    key: 'settings:maceprotection',
    type: 'bool'
  }, {
    key: 'settings:preventwebrtcleak',
    type: 'bool'
  }, {
    key: 'settings:rememberme',
    type: 'bool'
  }, {
    key: 'settings:firstRun',
    type: 'bool'
  }, {
    key: 'tiles',
    type: 'object'
  }];
}

function getKeys() {
  const modernKeys = ['storage::migrated', 'settings:alwaysActive'];
  const legacyKeys = getLegacyInfo().map(info => {
    return info.key;
  });
  return [...modernKeys, ...legacyKeys];
}
/**
 * copy a value
 *
 * @template T
 * @param {T} value
 *
 * @returns {T}
 */


function copyValue(value) {
  switch (typeof value) {
    // cannot handle undefined
    case 'undefined':
      return undefined;
    // primitives are passed as copied anyways

    case 'string':
      return value;

    case 'boolean':
      return value;

    case 'number':
      return value;
    // other (null/object), use JSON to copy

    default:
      return JSON.parse(JSON.stringify(value));
  }
}
/**
 * Storage
 *
 * Responsible for storing values using known keys either in
 * WebExtension storage (default) or in memory
 *
 * Under the covers, stores everything in memory but will backup
 * to WebExtension storage if persistence is desired
 *
 * At this time does not support dynamic keys
 *
 * The following are properties of Storage:
 * - "undefined" values are considered missing
 * - "null" values are considered present
 * - values stored are copies of the values given
 * - values retreived are copied of the values stored
 * - values are copied using: JSON.stringify -> JSON.parse, meaning:
 *   - circular objects will error out
 *   - functions will be stripped on stored object
 *   - items in storage are immutable (IMPORTANT, would present bugs otherwise)
 */


class storage_Storage {
  constructor() {
    // bindings
    this.hasItem = this.hasItem.bind(this);
    this.getItem = this.getItem.bind(this);
    this.setItem = this.setItem.bind(this);
    this.removeItem = this.removeItem.bind(this);
    this.init = this.init.bind(this);
    this.getItems = this.getItems.bind(this);
    this.store = {};
  }
  /*------------------------------------------*/

  /*                Public                    */

  /*------------------------------------------*/


  async init() {
    let migrated; // debug is not defined yet (depends on storage)

    const debug = msg => {
      if (Object(isDev["a" /* default */])()) {
        // eslint-disable-next-line no-console
        console.log(msg);
      }
    };

    try {
      migrated = await new Promise((resolve, reject) => {
        chrome.storage.local.get('storage::migrated', data => {
          if (chrome.runtime.lastError) {
            debug('storage.js: failed to determine migrated status');
            reject(chrome.runtime.lastError);
          } else {
            resolve(data['storage::migrated']);
          }
        });
      });
    } catch (_) {
      // if there is an error, user will lose previous data
      // but extension will continue to function
      // (they will need to login & set preferences again)
      migrated = true;
    }

    if (migrated) {
      // load items from persistent storage
      debug('storage.js: loading data from chrome.local');

      try {
        await new Promise((resolve, reject) => {
          chrome.storage.local.get(getKeys(), data => {
            if (chrome.runtime.lastError) {
              debug('storage.js: failed to retrieve items from persistent storage');
              reject(chrome.runtime.lastError);
            } else {
              Object.keys(data).forEach(key => {
                // all data keys should be strings
                if (key) {
                  this.store[key] = data[key];
                }
              });
              resolve();
            }
          });
        });
        debug('storage.js: successfully loaded data from chrome.local');
      } catch (err) {
        if (debug) {
          debug('storage.js: failed to load chrome.local');
          debug(err);
        }
      }
    } else {
      debug('storage.js: migrating');

      try {
        // move items from legacy storage to persistent storage
        const pendingMigration = getLegacyInfo().map(async ({
          key,
          type
        }) => {
          const fromLocalStorage = localStorage.getItem(key);

          if (fromLocalStorage === null) {
            return Promise.resolve();
          }

          if (typeof fromLocalStorage === 'undefined') {
            return Promise.resolve();
          }

          if (fromLocalStorage === '' && type !== 'string') {
            // empty string values for non-string types should be undefined
            return Promise.resolve();
          }

          switch (type) {
            case 'object':
              {
                return this.setItem(key, JSON.parse(fromLocalStorage));
              }

            case 'bool':
              {
                return this.setItem(key, fromLocalStorage === String(true));
              }

            case 'number':
              {
                return this.setItem(key, Number(fromLocalStorage));
              }

            case 'string':
              {
                return this.setItem(key, fromLocalStorage);
              }

            default:
              throw new Error(`storage: migration invalid type: ${type}`);
          }
        });
        await Promise.all(pendingMigration);
        await this.setItem('storage::migrated', true);
        window.localStorage.clear();
        debug('storage.js: successfully migrated data');
      } catch (err) {
        if (debug) {
          debug('storage.js: failed to migrate localStorage to chrome.storage.local');
          debug(err);
        }

        try {
          await this.setItem('storage::migrated', true);
        } catch (_) {
          /* noop */
        }
      }
    }
  }

  hasItem(key) {
    if (storage_Storage.validateKey(key)) {
      const item = this.getItem(key);
      return typeof item !== 'undefined';
    }

    throw storage_Storage.createOperationError('has');
  }

  getItem(key) {
    if (storage_Storage.validateKey(key)) {
      const value = this.store[key];
      return copyValue(value);
    }

    throw storage_Storage.createOperationError('get');
  }

  setItem(key, value) {
    // create a copy to work with
    const copy = copyValue(value);

    if (storage_Storage.validateKey(key)) {
      if (typeof copy === 'undefined') {
        debug(`storage.js: attempt to store undefined for key ${key}`);
        return;
      }

      this.store[key] = copy;
      chrome.storage.local.set({
        [key]: copy
      }, () => {
        if (chrome.runtime.lastError) {
          debug(`storage.js: failed to set ${key} in persistent storage`);
          debug(chrome.runtime.lastError);
        }
      });
      return;
    }

    throw storage_Storage.createOperationError('set');
  }

  removeItem(key) {
    if (storage_Storage.validateKey(key)) {
      delete this.store[key]; // remove from persistent storage if needed

      chrome.storage.local.remove(key, () => {
        if (chrome.runtime.lastError) {
          debug(`storage.js: failed to remove ${key} in persistent storage`);
          debug(chrome.runtime.lastError);
        }
      });
    } else {
      throw storage_Storage.createOperationError('remove');
    }
  }
  /**
   * Get items in store for debugging purposes
   *
   * @returns {string}
   */


  getItems() {
    return JSON.stringify(this.store, null, 2);
  }
  /*------------------------------------------*/

  /*                Static                    */

  /*------------------------------------------*/


  static validateKey(key) {
    const valid = !!getKeys().find(k => {
      return k === key;
    });

    if (!valid) {
      debug(`storage.js: invalid key: ${key}`);
    }

    return valid;
  }

  static validateStoreAndKey({
    store,
    key
  }) {
    return storage_Storage.validateStore(store) && storage_Storage.validateKey(key);
  }

  static createOperationError(operation) {
    // Refer to errors thrown in validateStore or validateKey
    return new Error(`could not call ${operation}Item, invalid store or key`);
  }

}

/* harmony default export */ var util_storage = (storage_Storage);
// EXTERNAL MODULE: ./src/js/firefoxsettings/storage.js
var firefoxsettings_storage = __webpack_require__(120);

// EXTERNAL MODULE: ./src/js/util/settings.js
var util_settings = __webpack_require__(122);

// EXTERNAL MODULE: ./src/js/util/icon.js
var icon = __webpack_require__(117);

// EXTERNAL MODULE: ./src/js/util/regionlist.js
var util_regionlist = __webpack_require__(125);

// EXTERNAL MODULE: ./src/js/util/regionsorter.js
var regionsorter = __webpack_require__(129);

// EXTERNAL MODULE: ./src/js/util/user.js
var util_user = __webpack_require__(116);

// EXTERNAL MODULE: ./src/js/util/bypasslist.js
var util_bypasslist = __webpack_require__(126);

// EXTERNAL MODULE: ./src/js/util/smart-location.js
var smart_location = __webpack_require__(131);

// EXTERNAL MODULE: ./src/js/util/latencymanager.js
var latencymanager = __webpack_require__(127);

// EXTERNAL MODULE: ./src/js/util/buildinfo.js
var buildinfo = __webpack_require__(124);

// EXTERNAL MODULE: ./src/js/util/logger.js
var logger = __webpack_require__(119);

// EXTERNAL MODULE: ./src/js/util/counter.js
var counter = __webpack_require__(121);

// EXTERNAL MODULE: ./src/js/util/settingsmanager.js
var util_settingsmanager = __webpack_require__(130);

// EXTERNAL MODULE: ./src/js/util/errorinfo.js
var errorinfo = __webpack_require__(123);

// EXTERNAL MODULE: ./src/js/util/i18n.js
var util_i18n = __webpack_require__(118);

// EXTERNAL MODULE: ./src/js/util/platforminfo.js
var platforminfo = __webpack_require__(128);

// EXTERNAL MODULE: ./src/js/data/https-upgrade.js
var https_upgrade = __webpack_require__(25);

// EXTERNAL MODULE: ./src/js/helpers/http.js
var http = __webpack_require__(15);

// EXTERNAL MODULE: ./src/js/helpers/timer.js
var timer = __webpack_require__(76);

// EXTERNAL MODULE: ./src/js/helpers/reportError.js
var reportError = __webpack_require__(64);

// CONCATENATED MODULE: ./src/js/util/https-upgrade/rulesets.js
/* eslint no-restricted-syntax: 0 */



 // ======================================== //
//                 General                  //
// ======================================== //

/**
 * Get the default channel for rulesets
 */

function getDefaultChannel() {
  return https_upgrade["k" /* channels */].find(c => {
    return c.name === 'default';
  });
}
/**
 * Attempt to apply a ruleset to a url
 *
 * @returns {string|undefined}
 */

function applyRuleset(ruleset, url) {
  const {
    rule: rules,
    exclusions
  } = ruleset;

  if (!rules) {
    return undefined;
  }

  if (typeof exclusions !== 'undefined') {
    if (exclusions instanceof RegExp) {
      if (exclusions.test(url)) {
        debug(`https-upgrade/rulesets#applyRuleset: ${url} excluded`);
        return undefined;
      }
    } else {
      debug('https-upgrade/rulesets#applyRuleset: invalid exclusions');
      debug(`typeof exclusions: ${typeof exclusions}`);
      debug(`exclusions value: ${exclusions}`);
    }
  }

  let applied;
  return rules.find(rule => {
    if (rule.to === null || rule.from === null) {
      return false;
    }

    applied = url.replace(new RegExp(rule.from), rule.to);
    return applied === url ? false : applied;
  }) && applied;
}

async function debugTime(name, fn) {
  const start = performance.now();
  const res = await Promise.resolve(fn());
  const end = performance.now();
  const duration = Math.floor(end - start);
  debug(`https-upgrade: ${name} took ${duration}ms`);
  return res;
} // ======================================== //
//                  Stored                  //
// ======================================== //

/**
 * Retrieve the stored rulesets from storage.local
 *
 * Break into multiple operations to avoid locking up the background thread
 *
 * @returns {*} rulesets
 */


async function getStoredRulesets(storageCount) {
  // validate storageCount
  if (!storageCount || Number.isNaN(Number(storageCount))) {
    throw new Error('invalid storage count value');
  } // generate keys


  const storageKeys = Array.from(new Array(Number(storageCount)).keys()).map(i => {
    return https_upgrade["j" /* STORAGE_TEMPLATE */].replace('%s', i);
  }); // for each key, generate op to retrieve part from storage

  const ops = storageKeys.map(key => {
    return async () => {
      const part = await new Promise((resolve, reject) => {
        chrome.storage.local.get(key, data => {
          if (chrome.runtime.lastError) {
            reject(chrome.runtime.lastError);
          } else {
            resolve(data[key]);
          }
        });
      }); // yield to event loop

      await Object(timer["a" /* default */])(5);
      return part;
    };
  });
  return debugTime('stage e', async () => {
    // perform ops consecutively
    const parts = [];

    for (const op of ops) {
      parts.push(await op());
    }

    return parts;
  });
}
/**
 * Store the rulesets in storage.local
 *
 * Break up the operations by parts to avoid locking up the background thread
 *
 * @param {Array} parts Storage payload
 * @param {number} oldCount Previous parts length
 */

async function setStoredRulesets(parts, oldCount) {
  // create ops to push each part into storage
  const addOps = parts.map((part, i) => {
    return async () => {
      await new Promise((resolve, reject) => {
        chrome.storage.local.set({
          [https_upgrade["j" /* STORAGE_TEMPLATE */].replace('%s', i)]: part
        }, () => {
          if (chrome.runtime.lastError) {
            reject(chrome.runtime.lastError);
          } else {
            resolve();
          }
        });
      }); // yield to event loop

      await Object(timer["a" /* default */])(5);
    };
  });

  const act = async () => {
    await debugTime('stage d (delete)', async () => {
      const oldCountNum = Number(oldCount); // delete excess parts in storage

      if (!Number.isNaN(oldCountNum) && oldCountNum > parts.length) {
        const keys = [...Array(oldCountNum - parts.length).keys()].map(i => {
          return i + parts.length;
        }).map(i => {
          return https_upgrade["j" /* STORAGE_TEMPLATE */].replace('%s', i);
        });
        await new Promise(resolve => {
          chrome.storage.local.remove(keys, () => {
            if (chrome.runtime.lastError) {
              const err = chrome.runtime.lastError;
              debug(`https-upgrade/rulesets#setStoredRulesets: failed to remove with "${err}"`);
            } else {
              resolve();
            }
          });
        });
      }
    });
    await debugTime('stage d (add)', async () => {
      // perform each add op consecutively
      for (const op of addOps) {
        // eslint-disable-next-line no-await-in-loop
        await op();
      }
    });
  };

  try {
    await act();
  } catch (err) {
    debug('https-upgrade/rulesets: stage d (store rulesets) failed');
    Object(reportError["a" /* default */])('https-upgrade/rulesets', err);
    debug('https-upgrade/rulesets: retry storing rulesets...');
    await Object(timer["a" /* default */])(5000);
    await act();
    debug('https-upgrade/rulesets: successfully stored rulesets');
  }
} // ======================================== //
//                  Hosted                  //
// ======================================== //

async function getTimestamp(channel) {
  const url = `${channel.urlPrefix}${https_upgrade["e" /* LATEST_TIMESTAMP_FILE */]}`;
  const res = await debugTime('stage a', () => {
    return http["a" /* default */].get(url);
  });

  if (!res.ok) {
    throw res;
  }

  const text = await res.text();
  const trimmed = text.trim();

  if (Number.isNaN(Number(trimmed))) {
    throw new Error('timestamp is not a number');
  }

  return trimmed;
}

async function getBuffer(channel) {
  const rulesFileUrl = `${channel.urlPrefix}${https_upgrade["h" /* RULESET_FILE_TEMPLATE */]}`;

  try {
    return await http["a" /* default */].get(rulesFileUrl).then(r => {
      return r.arrayBuffer();
    });
  } catch (err) {
    throw new Error('failed to fetch buffers');
  }
}
/**
 * Extract a compressed buffer
 *
 * Uses WebWorker because pako#inflate does not offer async API
 */


async function extract(rulesBuffer) {
  // Get url (same as ./worker.js file)
  const url = chrome.runtime.getURL('js/https-upgrade-worker.js');
  const worker = new Worker(url);
  const reqID = 0;
  return new Promise(resolve => {
    worker.addEventListener('message', e => {
      const {
        data: {
          payload,
          type
        }
      } = e;

      if (type === https_upgrade["f" /* MessageType */].EXTRACT_RES && payload.reqID === reqID) {
        const {
          extracted
        } = payload;
        worker.terminate();
        resolve(extracted);
      }
    });
    worker.postMessage({
      type: https_upgrade["f" /* MessageType */].EXTRACT_REQ,
      payload: {
        rulesBuffer,
        reqID
      }
    });
  });
}
/**
 * Fetch the rulesets from specified channel
 *
 * @returns {*} results
 * @returns {number} results.timestamp
 * @returns {*} results.rulesets
 */


async function getHostedRulesets(channel) {
  try {
    const buffer = await debugTime('stage b', () => {
      return getBuffer(channel);
    });
    let {
      rulesets
    } = await debugTime('stage c', () => {
      return extract(buffer);
    }); // Convert exclusions

    rulesets = rulesets.map(ruleset => {
      const {
        exclusion
      } = ruleset;

      if (Array.isArray(exclusion)) {
        return Object.assign({}, ruleset, {
          exclusions: new RegExp(exclusion.join('|')),
          exclusion: undefined
        });
      }

      if (exclusion) {
        debug('https-upgrade/index.js: failed to convert exclusion');
        debug(JSON.stringify(ruleset));
      }

      return ruleset;
    }); // break into parts

    const parts = [];

    while (rulesets.length) {
      parts.push(rulesets.splice(0, https_upgrade["g" /* PART_SIZE */]));
    }

    return parts;
  } catch (err) {
    debug(err.message || err.cause || err);
    throw err;
  }
} // ======================================== //
//                  Local                   //
// ======================================== //

/**
 * Convert list of rules to map of (target, ruleset) pairs
 *
 * @param {Array} parts
 *
 * @returns {Map}
 */

async function partsToTargetMap(parts) {
  const map = new Map();
  const ops = parts.map(part => {
    return async () => {
      part.forEach(ruleset => {
        if (!Array.isArray(ruleset.target)) {
          debug('https-rules: rule missing target array');
        } else {
          for (const target of ruleset.target) {
            if (!map.has(target)) {
              map.set(target, new Set());
            }

            map.get(target).add(ruleset);
          }
        }
      }); // yield to event loop (to prevent locking up background)
      // eslint-disable-next-line no-await-in-loop

      await Object(timer["a" /* default */])(5);
    };
  });
  await debugTime('stage f', async () => {
    for (const op of ops) {
      await op();
    }
  });
  return map;
}
// CONCATENATED MODULE: ./src/js/util/https-upgrade/index.js
/* eslint no-restricted-syntax: 0 */


/**
 * HttpsUpgrade Utility
 *
 * Will handle fetching & updating rulesets used to upgrade requests to
 * https protocol for improved security
 */

class https_upgrade_HttpsUpgrade {
  constructor(app) {
    // bind
    this.init = this.init.bind(this);
    this.enabled = this.enabled.bind(this);
    this.onAlarm = this.onAlarm.bind(this);
    this.attemptUpdate = this.attemptUpdate.bind(this);
    this.getPotentialRulesets = this.getPotentialRulesets.bind(this);
    this.onBeforeRequest = this.onBeforeRequest.bind(this);
    this.onCookieChanged = this.onCookieChanged.bind(this);
    this.onCompleted = this.onCompleted.bind(this);
    this.onErrorOccurred = this.onErrorOccurred.bind(this);
    this.onBeforeRedirect = this.onBeforeRedirect.bind(this); // init

    this.app = app;
    this.storage = app.util.storage;
    this.rulesets = new Map();
    this.rulesetsCache = new Map();
    this.counter = new Map();
    this.cookieCache = new Map();
    this.hrefBlacklist = new Set();
    this.updating = false;
    this.enabledTracker = false;
    this.upgradeToSecureAvailable = false;
    chrome.alarms.create(https_upgrade["a" /* ALARM_NAME */], {
      periodInMinutes: 30
    });
    this.initializing = this.init();
  }
  /**
   * Perform all necessary async initialization
   *
   * These operations could complete at ANY time after HttpsUpgrade
   * is instantiated, therefore the class must continue to function
   * properly before this has completed, and as it is completing
   *
   */


  async init() {
    const initOps = []; // break scope to allow constructor to complete

    await new Promise(resolve => {
      setTimeout(resolve, 0);
    });
    /*              Populate rules
     * The update is represented by 6 time consuming stages
     * A - Fetch the most recent timestamp
     * B - Fetch the corresponding rules to timestamp
     * C - Extract the rules
     * D - Store the rules in storage
     * E - Fetch rules from storage
     * F - Process the rules
     *
     * Some stages are skipped depending on whether or not the
     * rules are stored or whether the timestamp has changed
     */

    const op1 = (async () => {
      let fromLocation;
      const start = performance.now();
      let parts = await this.attemptUpdate();

      if (parts) {
        fromLocation = 'hosted';
      } else {
        fromLocation = 'stored';
        const storageCount = this.storage.getItem(https_upgrade["i" /* STORAGE_COUNT_KEY */]);
        parts = await getStoredRulesets(storageCount); // populate local rules (occurs in attemptUpdate)

        this.rulesetsCache.clear();
        this.rulesets = await partsToTargetMap(parts);
      } // calculate number of rules


      const numRules = parts.reduce((count, arr) => {
        return count + arr.length;
      }, 0); // debug info

      const end = performance.now();
      const duration = Math.floor(end - start);
      debug(`https-upgrade: populating ${numRules} ${fromLocation} rulesets took ${duration}ms`);
    })();

    initOps.push(op1);
    await Promise.all(initOps);
  }
  /**
   * Determine if the https-upgrade setting is enabled
   *
   * If this is not enabled, the various listeners should
   * not interfere/react when triggered. Also used for misc
   * cleanup after setting is disabled.
   */


  enabled() {
    const {
      app: {
        util: {
          settings
        }
      }
    } = this;
    const enabled = settings.isActive('httpsUpgrade');

    if (!enabled && this.enabledTracker) {
      this.counter.clear();
      this.cookieCache.clear();
    }

    this.enabledTracker = enabled;
    return enabled;
  }
  /**
   * Triggered when an alarm event occurs
   *
   * Attempt to update the rulesets
   */


  async onAlarm(alarm) {
    if (alarm.name === https_upgrade["a" /* ALARM_NAME */]) {
      await this.attemptUpdate();
    }

    return undefined;
  }
  /**
   * Attempt to fetch rulesets and store in persistent storage
   *
   * Will only update if the hosted timestamp has changed
   */


  async attemptUpdate() {
    if (this.updating) {
      debug('https-upgrade: cancelling update, update already in progress');
      return false;
    }
    /**
     * performUpdate will actually update the rulesets, regardless
     * of the currently stored timestamp
     */


    const performUpdate = async (channel, timestamp) => {
      this.updating = true;

      try {
        debug('https-upgrade: updating rulesets');
        const oldCount = this.storage.getItem(https_upgrade["i" /* STORAGE_COUNT_KEY */]);
        const parts = await getHostedRulesets(channel);
        this.rulesetsCache.clear();
        this.rulesets = await partsToTargetMap(parts); // set STORAGE_COUNT_KEY
        // in the event that the browser is closed BEFORE the timestamp is
        // updated, we still want to successfully cleanup any potential space

        const {
          length: count
        } = parts;
        this.storage.setItem(https_upgrade["i" /* STORAGE_COUNT_KEY */], count); // NOTE: if EU closes browser during this operation, we want
        // to always fetch the rulesets again

        await setStoredRulesets(parts, oldCount); // update timestamp only AFTER the operation completes successfully

        this.storage.setItem(https_upgrade["c" /* LAST_TIMESTAMP_KEY */], timestamp);
        this.storage.setItem(https_upgrade["i" /* STORAGE_COUNT_KEY */], count);
        this.storage.setItem(https_upgrade["d" /* LAST_UPDATED_KEY */], Date.now());
        this.updating = false;
        return parts;
      } catch (err) {
        this.updating = false;
        debug('https-upgrade: failed to update rulesets');
        debug(err.message || err);
        throw err;
      }
    };

    debug('https-upgrade: checking if update required');

    try {
      // get update channel
      const channel = getDefaultChannel(); // get remote timestamp

      const timestamp = await getTimestamp(channel); // get local timestamp

      const lastTimestamp = this.storage.getItem(https_upgrade["c" /* LAST_TIMESTAMP_KEY */]); // if no local timestamp (update has never occurred successfully), perform update

      if (!lastTimestamp) {
        return performUpdate(channel, timestamp);
      } // if timestamp has changed, perform update


      if (Number(timestamp) !== Number(lastTimestamp)) {
        return performUpdate(channel, timestamp);
      } // timestamp is up to date, do not update


      debug('https-upgrade: postponing https update');
      return false;
    } catch (err) {
      debug('https-upgrade: failed to update');
      debug(err.message || err);
      throw err;
    }
  }
  /**
   * Fetch the rulesets that might apply to a specific domain
   */


  getPotentialRulesets(domain) {
    const isValidDomain = target => {
      if (target.length <= 0) {
        return false;
      }

      if (target.length > 255) {
        return false;
      }

      if (target.includes('..')) {
        return false;
      }

      return true;
    };

    const getRulesets = target => {
      let rulesets = this.rulesetsCache.get(target);

      if (!rulesets) {
        rulesets = this.rulesets.get(target);
        this.rulesetsCache.set(target, rulesets);
      }

      return rulesets;
    }; // example domain "x.y.z.domain.com"


    const results = new Set();

    if (isValidDomain(domain)) {
      // search for "x.y.z.domain.com"
      const exactMatches = getRulesets(domain);

      if (exactMatches) {
        exactMatches.forEach(exactMatch => {
          results.add(exactMatch);
        });
      } // search for
      // "*.y.z.domain.com"
      // "*.z.domain.com"
      // "*.domain.com"


      const splits = domain.split('.');

      if (splits.length > 2) {
        const root = splits.slice(-2).join('.');
        let subdomains = splits.slice(0, -2);
        subdomains.push('');

        while (subdomains.length > 1) {
          subdomains = subdomains.slice(1);
          const target = `*.${subdomains.join('.')}${root}`;
          const matches = getRulesets(target);

          if (matches) {
            matches.forEach(match => {
              results.add(match);
            });
          }
        }
      }
    } else {
      debug(`https-upgrade: invalid domain for rulesets "${domain}"`);
    }

    results.delete(undefined);
    return Array.from(results.values());
  }

  shouldSecureCookie(cookie) {
    let shouldSecure = false;
    let {
      domain
    } = cookie;

    if (this.cookieCache.size > 300) {
      this.cookieCache.delete(this.cookieCache.keys().next().value);
    }

    while (domain.charAt(0) === '.') {
      domain = domain.slice(1);
    }

    const potentialRules = this.getPotentialRulesets(domain); // check cache

    const cacheItem = this.cookieCache.get(domain);

    if (cacheItem) {
      shouldSecure = true;
    } // update cache
    else {
        const fakeUrl = `http://${domain}/${Math.random()}/${Math.random()}`;
        shouldSecure = !!potentialRules.find(ruleset => {
          if (applyRuleset(ruleset, fakeUrl)) {
            this.cookieCache.set(domain, true);
            return true;
          }

          return false;
        });

        if (!shouldSecure) {
          this.cookieCache.set(domain, false);
        }
      }

    if (!shouldSecure) {
      return false;
    }

    return potentialRules.filter(ruleset => {
      return ruleset.securecookie;
    }).find(ruleset => {
      return ruleset.securecookie.find(cr => {
        return !!(new RegExp(cr.host).test(cookie.domain) && new RegExp(cr.name).test(cookie.name));
      });
    });
  } // ======================================== //
  //                Listeners                 //
  // ======================================== //

  /**
   * Upgrade url to https if a matching rule is found
   */


  onBeforeRequest(details) {
    if (this.enabled()) {
      let username = '';
      let password = '';

      if (!details.url) {
        return undefined;
      }

      const url = new URL(details.url); // Strip trailing '.'

      while (url.hostname.endsWith('.') && url.hostname.length > 1) {
        url.hostname = url.hostname.slice(0, url.hostname.length - 1);
      }

      if (url.username || url.password) {
        ({
          username,
          password
        } = url);
        url.username = '';
        url.password = '';
      }

      if (this.hrefBlacklist.has(url.href)) {
        return undefined;
      }

      if (this.counter.get(details.requestId) >= https_upgrade["b" /* COUNTER_LIMIT */]) {
        debug(`https-upgrade: blacklisting href "${url.href}"`);
        this.hrefBlacklist.add(url.href);
        return undefined;
      }

      const [matchedRuleset] = this.getPotentialRulesets(url.hostname);

      if (matchedRuleset) {
        let upgradedUrl = applyRuleset(matchedRuleset, url.href);

        if (!upgradedUrl) {
          return undefined;
        }

        if (username || password) {
          const withCredentials = new URL(upgradedUrl);
          withCredentials.username = username;
          withCredentials.password = password;
          upgradedUrl = withCredentials.href;
        }

        if (this.upgradeToSecureAvailable && upgradedUrl === details.url.replace(/^http:/, 'https:')) {
          debug(`https-upgrade: upgrading ${details.url} using upgradeToSecure API`);
          return {
            upgradeToSecure: true
          };
        }

        debug(`https-upgrade: redirecting ${details.url} to ${upgradedUrl}`);
        return {
          redirectUrl: upgradedUrl
        };
      }
    }

    return undefined;
  }
  /**
   * Secure insecure cookies
   */


  onCookieChanged(details) {
    if (this.enabled()) {
      const {
        cookie
      } = details;

      if (!details.removed && !cookie.secure && this.shouldSecureCookie(cookie)) {
        debug(`https-upgrade: attempting to secure cookie: ${cookie.name}`);
        const secureCookie = Object.assign({
          name: cookie.name,
          value: cookie.value,
          path: cookie.path,
          httpOnly: cookie.httpOnly,
          expirationDate: cookie.expirationDate,
          storeId: cookie.storeId,
          secure: true
        }, cookie.hostOnly ? {} : {
          domain: cookie.domain
        }, // https://tools.ietf.org/html/draft-west-first-party-cookies
        cookie.sameSite ? {
          sameSite: cookie.sameSite
        } : {}, cookie.firstPartyDomain ? {
          firstPartyDomain: cookie.firstPartyDomain
        } : {}, cookie.domain.startsWith('.') ? {
          url: `https://www${cookie.domain}${cookie.path}`
        } : {
          url: `https://${cookie.domain}${cookie.path}`
        });
        chrome.cookies.set(secureCookie);
        debug(`https-upgrade: secured cookie "${cookie.name}" for "${cookie.domain}"`);
      }
    }
  }
  /**
   * Handle counter on request completion
   */


  onCompleted(details) {
    if (this.enabled()) {
      const {
        requestId
      } = details;

      if (this.counter.has(requestId)) {
        this.counter.delete(requestId);
        debug(`https-upgrade: clearing count for ${requestId}`);
      }
    }
  }
  /**
   * Handle counter on request error
   */


  onErrorOccurred(details) {
    if (this.enabled()) {
      if (this.counter.has(details.requestId)) {
        this.counter.delete(details.requestId);
      }
    }
  }
  /**
   * Handle counter for redirects (prevent looping)
   */


  onBeforeRedirect(details) {
    if (this.enabled()) {
      if (details.redirectUrl.match(/^https?:\/\/.*/)) {
        const {
          requestId
        } = details;
        const oldCount = https_upgrade_HttpsUpgrade.parseCount(this.counter, requestId);
        this.counter.set(requestId, oldCount + 1);
        debug(`https-upgrade: increment count for ${requestId} to ${oldCount + 1}`);
      }
    }
  } // ======================================== //
  //                  Static                  //
  // ======================================== //


  static parseCount(counter, requestId) {
    const value = counter.get(requestId);

    if (typeof value === 'undefined') {
      return 0;
    }

    if (typeof value === 'number' && value >= 0) {
      return value;
    }

    debug(`https-upgrade: request count for ${requestId} invalid: ${value}`);
    return 0;
  }

}

/* harmony default export */ var util_https_upgrade = (https_upgrade_HttpsUpgrade);
// EXTERNAL MODULE: ./src/js/util/ipmanager.js
var ipmanager = __webpack_require__(132);

// EXTERNAL MODULE: ./src/js/helpers/messagingFirefox.js
var messagingFirefox = __webpack_require__(4);

// CONCATENATED MODULE: ./src/js/mockapp/mockAppAdapter.js

class mockAppAdapter_MockAppAdapter {
  constructor(app) {
    // properties
    this.app = app;
    this.target = messagingFirefox["Target"].FOREGROUND; // bindings

    this.initialize = this.initialize.bind(this);
    this.sendMessage = this.sendMessage.bind(this);
    this.handleMessage = this.handleMessage.bind(this);
    this.handleRegionList = this.handleRegionList.bind(this);
    console.log('SENT MESSAGE -------------', this.handleMessage); // handle listener

    browser.runtime.onMessage.addListener(this.handleMessage);
  }

  handleMessage(message, sender, response) {
    if (!Object(messagingFirefox["isTarget"])(message, messagingFirefox["Target"].BACKGROUND)) {
      return false;
    } // can't return a promise because it's the polyfill version
    // and firefox won't recognize it as a "real" promise


    new Promise(resolve => {
      let res = {};

      if (message.type === 'initialize') {
        res = this.initialize();
      } else if (message.type === 'util.user.setUsername') {
        const {
          username
        } = message.data;
        this.app.util.user.setUsername(username);
      } else if (message.type === 'util.user.setAccount') {
        this.app.util.user.setAccount(message.data);
      } else if (message.type === 'util.user.setRememberMe') {
        const {
          rememberMe
        } = message.data;
        this.app.util.user.setRememberMe(rememberMe);
      } else if (message.type === 'util.user.setLoggedIn') {
        const {
          value
        } = message.data;
        this.app.util.user.setLoggedIn(value);
      } else if (message.type === 'util.user.setAuthToken') {
        const {
          authToken
        } = message.data;
        this.app.util.user.setAuthToken(authToken);
      } else if (message.type === 'updateSettings') {
        const {
          settingID,
          value
        } = message.data;
        this.app.util.settings.setItem(settingID, value, true);
      } else if (message.type === 'smartLocation') {
        const {
          settingID,
          value
        } = message.data;
        this.app.util.smartlocation.saveToStorage(settingID, value, true);
      } else if (message.type === 'sameApp') {
        const {
          settingID
        } = message.data;
        this.app.sameApp.saveToStorage(settingID, value, true);
      } else if (message.type === 'util.settings.toggle') {
        const {
          settingID
        } = message.data;
        this.app.util.settings.toggle(settingID, true);
      } else if (message.type === 'enablePopularRule') {
        if (message.data.restartProxy === false) {
          this.app.util.bypasslist.enablePopularRule(message.data.name, true, false);
        } else {
          this.app.util.bypasslist.enablePopularRule(message.data.name, true);
        }
      } else if (message.type === 'disablePopularRule') {
        if (message.data.restartProxy === false) {
          this.app.util.bypasslist.disablePopularRule(message.data.name, true, false);
        } else {
          this.app.util.bypasslist.disablePopularRule(message.data.name, true);
        }
      } else if (message.type === 'setUserRules') {
        this.app.util.bypasslist.setUserRules(message.data, true);
      } else if (message.type === 'tiles') {
        this.app.util.storage.setItem('tiles', JSON.stringify(message.data));
      } else if (message.type === 'drawerState') {
        this.app.util.storage.setItem('drawerState', message.data);
      } else if (message.type === messagingFirefox["Type"].DEBUG) {
        const {
          data: {
            debugMsg
          }
        } = message;
        debug(debugMsg);
      } else if (message.type.startsWith(messagingFirefox["Namespace"].REGIONLIST)) {
        res = this.handleRegionList(message);
      } else if (message.type.startsWith(messagingFirefox["Namespace"].PROXY)) {
        res = this.handleProxyMessage(message);
      } else if (message.type.startsWith(messagingFirefox["Namespace"].BYPASSLIST)) {
        res = this.handleBypasslistMessage(message);
      } else if (message.type.startsWith(messagingFirefox["Namespace"].I18N)) {
        res = this.handleI18nMessage(message);
      }

      return resolve(res);
    }).then(response).catch(() => {
      return response(false);
    }); // must return true here to keep the response callback alive

    return true;
  }

  handleI18nMessage(message) {
    return Promise.resolve(message).then(({
      data,
      type
    }) => {
      const {
        util: {
          i18n
        }
      } = this.app;

      switch (type) {
        case messagingFirefox["Type"].I18N_TRANSLATE:
          {
            const {
              key,
              opts = {}
            } = data;
            return i18n.t(key, opts);
          }

        default:
          throw new Error(`no handler for type ${type}`);
      }
    });
  }
  /**
   * Handle messages directed to regionlist
   */


  handleRegionList(message) {
    return Promise.resolve(message).then(({
      data,
      type
    }) => {
      const {
        regionlist
      } = this.app.util;

      switch (type) {
        case messagingFirefox["Type"].SET_SELECTED_REGION:
          {
            const {
              id
            } = data;
            return regionlist.setSelectedRegion(id, true);
          }

        case messagingFirefox["Type"].IMPORT_REGIONS:
          {
            return regionlist.import(data);
          }

        case messagingFirefox["Type"].IMPORT_AUTO_REGION:
          {
            return regionlist.importAutoRegion(data, true);
          }

        case messagingFirefox["Type"].SET_FAVORITE_REGION:
          {
            return regionlist.setFavoriteRegion(data, true);
          }

        case messagingFirefox["Type"].ADD_OVERRIDE_REGION:
          {
            return regionlist.addOverrideRegion(data, true);
          }

        case messagingFirefox["Type"].REMOVE_OVERRIDE_REGION:
          {
            return regionlist.removeOverrideRegion(data, true);
          }

        default:
          throw new Error(`no handler for ${type}`);
      }
    });
  }

  handleProxyMessage(message) {
    return Promise.resolve(message).then(async ({
      type
    }) => {
      const {
        proxy
      } = this.app;

      switch (type) {
        case messagingFirefox["Type"].PROXY_ENABLE:
          {
            await proxy.enable();
            return;
          }

        case messagingFirefox["Type"].PROXY_DISABLE:
          {
            await proxy.disable();
            return;
          }

        default:
          throw new Error(`no handler for type '${type}'`);
      }
    });
  }

  handleBypasslistMessage(message) {
    return Promise.resolve(message).then(async ({
      type,
      data
    }) => {
      const {
        util: {
          bypasslist
        }
      } = this.app;

      switch (type) {
        case messagingFirefox["Type"].DOWNLOAD_BYPASS_JSON:
          {
            await bypasslist.saveRulesToFile();
            return;
          }

        case messagingFirefox["Type"].IMPORT_RULES:
          {
            const {
              rules
            } = data;
            bypasslist.importRules(rules);
          }

        default:
          throw new Error(`no handler for type: ${type}`);
      }
    });
  }

  initialize() {
    const isAuto = this.app.util.regionlist.getIsAuto();
    const regionId = this.app.util.regionlist.getSelectedRegion().id;
    const id = isAuto ? 'auto' : regionId;
    const payload = {
      proxy: {
        levelOfControl: this.app.proxy.getLevelOfControl(),
        enabled: this.app.proxy.enabled()
      },
      online: this.app.util.storage.getItem('online'),
      util: {
        user: {
          account: this.app.util.user.account,
          loggedIn: this.app.util.user.loggedIn,
          username: this.app.util.user.getUsername(),
          authToken: this.app.util.user.getAuthToken()
        },
        regionlist: {
          region: {
            id
          },
          regions: this.app.util.regionlist.export(),
          isAuto: this.app.util.regionlist.getIsAuto(),
          autoRegion: this.app.util.regionlist.exportAutoRegion(),
          favorites: this.app.util.storage.getItem('favoriteregions')
        },
        bypasslist: {
          user: this.app.util.bypasslist.getUserRules(),
          popular: this.app.util.bypasslist.enabledPopularRules().join(',')
        },
        smartlocation: {
          smartLocationRules: this.app.util.smartlocation.getSmartLocationRules('smartLocationRules'),
          checkSmartLocation: this.app.util.smartlocation.getSmartLocationRules('checkSmartLocation')
        },
        settings: this.app.util.settings.getAll()
      },
      sameApp: {
        sameAppBrowser: this.app.sameApp.returnBrowser()
      }
    };
    const tiles = this.app.util.storage.getItem('tiles');
    const drawerState = this.app.util.storage.getItem('drawerState');

    if (tiles) {
      try {
        payload.tiles = tiles;
      } catch (err) {
        /* noop */
      }
    }

    if (drawerState) {
      try {
        payload.drawerState = drawerState;
      } catch (err) {
        /* noop */
      }
    }

    return payload;
  }

  sendMessage(type, data) {
    return Object(messagingFirefox["sendMessage"])(this.target, type, data).catch(err => {
      if (!err.message) {
        throw err;
      }

      if (err.message.startsWith('Could not establish connection')) {
        return;
      }

      throw err;
    });
  }

}
// CONCATENATED MODULE: ./src/js/contentsettings/contentsetting.js
/*
   This object wraps a ContentSetting: https://developer.chrome.com/extensions/contentSettings#type-ContentSetting.
   Similar to but not the same as a ChromeSetting.
*/
/* harmony default export */ var contentsetting = (function (app, contentSetting) {
  const self = Object.create(null);
  const defaultSetRules = {
    primaryPattern: '<all_urls>',
    scope: 'regular'
  };
  const defaultClearRules = {
    scope: 'regular'
  };
  let applied;
  let ask;
  let blocked;
  let allowed;

  self.isApplied = () => {
    return applied;
  };

  self.isAsk = () => {
    return ask;
  };

  self.isBlocked = () => {
    return blocked;
  };

  self.isAllowed = () => {
    return allowed;
  };

  self._set = rules => {
    return new Promise((resolve, reject) => {
      contentSetting.set(Object.assign({}, defaultSetRules, rules), () => {
        if (chrome.runtime.lastError === undefined) {
          applied = true;
          ask = rules.setting === 'ask';
          blocked = rules.setting === 'block';
          allowed = rules.setting === 'allow';
          resolve();
        } else {
          reject(chrome.runtime.lastError);
        }
      });
    });
  };

  self._clear = (rules = {}) => {
    const {
      settingsmanager
    } = app.util;
    return new Promise((resolve, reject) => {
      contentSetting.clear(Object.assign({}, defaultClearRules, rules), () => {
        if (chrome.runtime.lastError === undefined) {
          blocked = false;
          allowed = false;
          ask = false;
          applied = false;
          settingsmanager.reapply(app.contentsettings);
          resolve();
        } else {
          reject(chrome.runtime.lastError);
        }
      });
    });
  };

  return self;
});
// CONCATENATED MODULE: ./src/js/contentsettings/microphone.js

/* harmony default export */ var microphone = (function (app) {
  const self = Object.create(contentsetting(app, chrome.contentSettings.microphone));
  self.settingID = 'blockmicrophone';
  self.settingDefault = false;

  self.applySetting = () => {
    return self._set({
      setting: 'block'
    }).then(() => {
      debug(`microphone.js: block ok`);
      return self;
    }).catch(error => {
      debug(`microphone.js: block failed (${error})`);
      return self;
    });
  };

  self.clearSetting = () => {
    return self._clear({}).then(() => {
      debug('microphone.js: unblock ok');
      return self;
    }).catch(error => {
      debug(`microphone.js: unblock failed (${error})`);
      return self;
    });
  };

  return self;
});
// CONCATENATED MODULE: ./src/js/contentsettings/camera.js

/* harmony default export */ var camera = (function (app) {
  const self = Object.create(contentsetting(app, chrome.contentSettings.camera));
  self.settingID = 'blockcamera';
  self.settingDefault = false;

  self.applySetting = () => {
    return self._set({
      setting: 'block'
    }).then(() => {
      debug(`camera.js: block ok`);
      return self;
    }).catch(error => {
      debug(`camera.js: block failed (${error})`);
      return self;
    });
  };

  self.clearSetting = () => {
    return self._clear({}).then(() => {
      debug('camera.js: unblock ok');
      return self;
    }).catch(error => {
      debug(`camera.js: unblock failed(${error})`);
      return self;
    });
  };

  return self;
});
// CONCATENATED MODULE: ./src/js/contentsettings/location.js

/* harmony default export */ var contentsettings_location = (function (app) {
  const self = Object.create(contentsetting(app, chrome.contentSettings.location));
  self.settingID = 'blocklocation';
  self.settingDefault = false;

  self.applySetting = () => {
    return self._set({
      setting: 'block'
    }).then(() => {
      debug(`location.js: block ok`);
      return self;
    }).catch(error => {
      debug(`location.js: block failed (${error})`);
      return self;
    });
  };

  self.clearSetting = () => {
    return self._clear({}).then(() => {
      debug('location.js: unblock ok');
      return self;
    }).catch(error => {
      debug(`location.js: unblock failed (${error})`);
      return self;
    });
  };

  return self;
});
// CONCATENATED MODULE: ./src/js/contentsettings/extension_notification.js

/* harmony default export */ var extension_notification = (function (app) {
  const defaultOptions = {
    icon: '/images/icons/icon64.png'
  };
  const self = Object.create(contentsetting(app, chrome.contentSettings.notifications));
  const {
    settings
  } = app.util;
  self.settingID = 'allowExtensionNotifications';
  self.settingDefault = true;
  self.alwaysActive = true;

  self.applySetting = () => {
    return self._set({
      setting: 'allow',
      primaryPattern: `*://${chrome.runtime.id}/*`
    }).then(() => {
      debug(`extensionNotification.js: allow ok`);
      return self;
    }).catch(error => {
      debug(`extensionNotification.js: allow failed (${error})`);
      return self;
    });
  };

  self.clearSetting = () => {
    return self._clear({}).then(() => {
      debug('extensionNotification.js: clear ok');
      return self;
    }).catch(error => {
      debug(`extensionNotification.js: clear failed (${error})`);
      return self;
    });
  };

  self.create = (title, options) => {
    if (!self.isAllowed()) {
      debug('extensionNotification.js: create failed (disabled).');
    } else {
      debug('extensionNotification.js: create notification');
      new Notification(title, Object.assign({}, defaultOptions, options));
    }
  };

  self.init = () => {
    if (!settings.hasItem(self.settingID) || settings.getItem(self.settingID)) {
      self.applySetting();
    }
  };

  return self;
});
// EXTERNAL MODULE: ./src/js/chromesettings/chromesetting.js
var chromesetting = __webpack_require__(23);

// CONCATENATED MODULE: ./src/js/chromesettings/hyperlinkaudit.js


class hyperlinkaudit_HyperLinkAudit extends chromesetting["a" /* default */] {
  constructor() {
    super(chrome.privacy.websites.hyperlinkAuditingEnabled); // bindings

    this.onChange = this.onChange.bind(this); // functions

    this.applySetting = this.createApplySetting(false, 'hyperlinkaudit', 'block');
    this.clearSetting = this.createClearSetting('hyperlinkaudit', 'unblock'); // init

    this.settingID = 'blockhyperlinkaudit';
    this.settingDefault = false;
  }

  onChange(details) {
    this.setLevelOfControl(details.levelOfControl);
    this.setBlocked(details.value === false);
  }

}

/* harmony default export */ var hyperlinkaudit = (hyperlinkaudit_HyperLinkAudit);
// CONCATENATED MODULE: ./src/js/chromesettings/webrtc.js


class webrtc_WebRTCSetting extends chromesetting["a" /* default */] {
  constructor() {
    super(chrome.privacy.network.webRTCIPHandlingPolicy); // bindings

    this.init = this.init.bind(this);
    this.onChange = this.onChange.bind(this); // functions

    this.applySetting = this.createApplySetting('disable_non_proxied_udp', 'webrtc', 'block');
    this.clearSetting = this.createClearSetting('webrtc', 'unblock'); // init

    this.settingID = 'preventwebrtcleak';
    this.settingDefault = false;
  }

  init() {
    this.blockable = chrome.privacy.network.webRTCIPHandlingPolicy !== undefined;
    super.init();
  }

  onChange(details) {
    this.levelOfControl = details.levelOfControl;
    this.blocked = details.value === 'disable_non_proxied_udp';
  }

}

/* harmony default export */ var webrtc = (webrtc_WebRTCSetting);
// CONCATENATED MODULE: ./src/js/chromesettings/thirdpartycookies.js


class thirdpartycookies_ThirdPartyCookies extends chromesetting["a" /* default */] {
  constructor() {
    super(chrome.privacy.websites.thirdPartyCookiesAllowed); // bindings

    this.onChange = this.onChange.bind(this); // functions

    this.applySetting = this.createApplySetting(false, 'thirdpartycookies', 'block');
    this.clearSetting = this.createClearSetting('thirdpartycookies', 'unblock'); // init

    this.settingID = 'blockthirdpartycookies';
    this.settingDefault = false;
  } // eslint-disable-next-line class-methods-use-this


  onChange(details) {
    this.setLevelOfControl(details.levelOfControl);
    this.setBlocked(details.value === false);
  }

}

/* harmony default export */ var thirdpartycookies = (thirdpartycookies_ThirdPartyCookies);
// CONCATENATED MODULE: ./src/js/chromesettings/httpreferer.js


class httpreferer_HttpReferer extends chromesetting["a" /* default */] {
  constructor() {
    super(chrome.privacy.websites.referrersEnabled); // bindings

    this.onChange = this.onChange.bind(this); // functions

    this.applySetting = this.createApplySetting(false, 'httpreferer', 'block');
    this.clearSetting = this.createClearSetting('httpreferer', 'unblock'); // init

    this.settingID = 'blockreferer';
    this.settingDefault = false;
  }

  onChange(details) {
    this.setLevelOfControl(details.levelOfControl);
    this.setBlocked(details.value === false);
  }

}

/* harmony default export */ var httpreferer = (httpreferer_HttpReferer);
// CONCATENATED MODULE: ./src/js/chromesettings/networkprediction.js


class networkprediction_NetworkPrediction extends chromesetting["a" /* default */] {
  constructor() {
    super(chrome.privacy.network.networkPredictionEnabled); // bindings

    this.onChange = this.onChange.bind(this); // functions

    this.applySetting = this.createApplySetting(false, 'networkprediction', 'block');
    this.clearSetting = this.createClearSetting('networkprediction', 'unblock'); // init

    this.settingID = 'blocknetworkprediction';
    this.settingDefault = false;
  }

  onChange(details) {
    this.setLevelOfControl(details.levelOfControl);
    this.setBlocked(details.value === false);
  }

}

/* harmony default export */ var networkprediction = (networkprediction_NetworkPrediction);
// CONCATENATED MODULE: ./src/js/chromesettings/safebrowsing.js


class safebrowsing_SafeBrowsing extends chromesetting["a" /* default */] {
  constructor() {
    super(chrome.privacy.services.safeBrowsingEnabled); // bindings

    this.onChange = this.onChange.bind(this); // functions

    this.applySetting = this.createApplySetting(false, 'safebrowsing', 'block');
    this.clearSetting = this.createClearSetting('safebrowsing', 'unblock'); // init

    this.settingID = 'blocksafebrowsing';
    this.settingDefault = false;
  }

  onChange(details) {
    this.setLevelOfControl(details.levelOfControl);
    this.setBlocked(details.value === false);
  }

}

/* harmony default export */ var safebrowsing = (safebrowsing_SafeBrowsing);
// CONCATENATED MODULE: ./src/js/chromesettings/proxy.js


const ONLINE_KEY = 'online';

const pacengine = __webpack_require__(104);

class proxy_BrowserProxy extends chromesetting["a" /* default */] {
  constructor(app) {
    super(chrome.proxy.settings); // bindings

    this.onChange = this.onChange.bind(this);
    this.settingsInMemory = this.settingsInMemory.bind(this);
    this.enabled = this.enabled.bind(this);
    this.readSettings = this.readSettings.bind(this);
    this.enable = this.enable.bind(this);
    this.filterByRemovedLocation = this.filterByRemovedLocation.bind(this);
    this.disable = this.disable.bind(this);
    this.getEnabled = this.getEnabled.bind(this);
    this.getProxyType = this.getProxyType.bind(this);
    this.setProxyType = this.setProxyType.bind(this); // init

    this.app = app;
    this.settingID = 'proxy';
    this.areSettingsInMemory = false;
    this.rules = []; // test data

    this.changing = false;
  }

  setProxyType(mode) {
    this.proxyType = mode;
  }

  getProxyType() {
    return this.proxyType;
  }

  settingsInMemory() {
    return this.areSettingsInMemory;
  }

  getEnabled() {
    if (this.getProxyType() === 'fixed_servers' || this.getProxyType() === 'pac_script') {
      return this.getProxyType();
    }
  }

  enabled() {
    return this.getEnabled();
  }

  async readSettings() {
    await this.get();
    proxy_BrowserProxy.debug('read settings');
    return this;
  }

  filterByRemovedLocation(location) {
    // filter rules by location
    if (location) {
      this.rules = this.rules.filter(rule => {
        return rule.cc != location.userSelect;
      });
    }
  }

  async enable() {
    const didChange = !this.getEnabled();
    this.changing = true;
    const key = app.util.regionlist.getPort();

    try {
      const {
        bypasslist,
        settings,
        regionlist,
        ipManager,
        smartlocation
      } = this.app.util;
      const locations = Object.values(regionlist.getRegions()); //get dictionary

      const nodeDict = pacengine.getNodeDictFromLocations(locations, key);
      let userRulesSmartLoc;

      if (smartlocation.getSmartLocationRules('smartLocationRules')) {
        userRulesSmartLoc = smartlocation.getSmartLocationRules('smartLocationRules').map(loc => {
          return {
            cc: loc.proxy.id,
            domain: loc.userRules,
            country: loc
          };
        });
      }

      const region = regionlist.getSelectedRegion();

      if (didChange) {
        try {
          await ipManager.update({
            retry: false
          });
        } catch (_) {
          debug('proxy: failed to update ip before enabling');
        }
      }

      let value = {};

      if (smartlocation.getSmartLocationRules('smartLocationRules').length > 0 && smartlocation.getSmartLocationRules('checkSmartLocation')) {
        this.rules = userRulesSmartLoc;
        const pacScript = pacengine.exportPAC(region.id, nodeDict, userRulesSmartLoc, bypasslist.getRulesSmartLoc()); //get the pac script

        value = {
          mode: 'pac_script',
          pacScript: {
            data: pacScript
          }
        };
      } else {
        const port = region[key];
        const proxyRule = proxy_BrowserProxy.createProxyRule(region, port);
        value = {
          mode: 'fixed_servers',
          rules: {
            singleProxy: proxyRule,
            bypassList: bypasslist.toArray()
          }
        };
      }

      await this.set({
        value
      }); // Make request immediately to force handshake to proxy server
      // Necessary because we cannot perform our side of handshake on
      // Chrome pages for security reasons

      http["a" /* default */].head('https://privateinternetaccess.com'); // trigger ip update

      ipManager.update({
        retry: true
      });
      proxy_BrowserProxy.debug('enabled');
      this.changing = false;
      return this;
    } catch (err) {
      this.changing = false;
      throw err;
    }
  }

  async disable() {
    const didChange = this.getEnabled();
    this.changing = true;
    const {
      ipManager
    } = this.app.util;

    try {
      await this.clear();

      if (didChange) {
        ipManager.update({
          retry: true
        });
      }

      proxy_BrowserProxy.debug('disabled');
      this.changing = false;
      return this;
    } catch (err) {
      this.changing = false;
      throw err;
    }
  }

  onChange(details) {
    const {
      util: {
        storage,
        icon,
        settingsmanager
      }
    } = this.app;
    this.setLevelOfControl(details.levelOfControl);
    this.setProxyType(details.value.mode);
    this.setBlocked(false);

    if (this.getEnabled()) {
      settingsmanager.enable();
      icon.online();
      storage.setItem(ONLINE_KEY, true);
    } else {
      settingsmanager.disable();
      icon.offline();
      storage.setItem(ONLINE_KEY, false);
    }

    settingsmanager.clearAndReapplySettings(); // eslint-disable-next-line no-param-reassign

    this.areSettingsInMemory = true;
  }

  static createProxyRule(region, port) {
    return {
      scheme: region.scheme,
      host: region.host,
      port
    };
  }

  static debug(msg, err) {
    return chromesetting["a" /* default */].debug('proxy', msg, err);
  }

}

/* harmony default export */ var chromesettings_proxy = (proxy_BrowserProxy);
// CONCATENATED MODULE: ./src/js/chromesettings/autofill.js


class autofill_AutoFill extends chromesetting["a" /* default */] {
  constructor() {
    super(chrome.privacy.services.autofillEnabled); // bindings

    this.onChange = this.onChange.bind(this); // functions

    this.applySetting = this.createApplySetting(false, 'autofill', 'block');
    this.clearSetting = this.createClearSetting('autofill', 'unblock'); // init

    this.settingID = 'blockautofill';
    this.settingDefault = false;
  } // eslint-disable-next-line class-methods-use-this


  isAvailable() {
    return !chrome.privacy.services.autofillAddressEnabled && !chrome.privacy.services.autofillCreditCardEnabled;
  } // eslint-disable-next-line class-methods-use-this


  onChange(details) {
    this.setLevelOfControl(details.levelOfControl);
    this.setBlocked(details.value === false);
  }

}

/* harmony default export */ var autofill = (autofill_AutoFill);
// CONCATENATED MODULE: ./src/js/chromesettings/autofillcreditcard.js


class autofillcreditcard_AutoFillCreditCard extends chromesetting["a" /* default */] {
  constructor(storage) {
    super(chrome.privacy.services.autofillCreditCardEnabled); // bindings

    this.onChange = this.onChange.bind(this); // functions

    this.applySetting = this.createApplySetting(false, 'autofillcreditcard', 'block');
    this.clearSetting = this.createClearSetting('autofillcreditcard', 'unblock'); // init

    this.settingID = 'blockautofillcreditcard';

    if (storage.getItem('settings:blockautofill')) {
      this.settingDefault = false;
    } else {
      this.settingDefault = false;
    }
  }

  onChange(details) {
    this.setLevelOfControl(details.levelOfControl);
    this.setBlocked(details.value === false);
  }

}

/* harmony default export */ var autofillcreditcard = (autofillcreditcard_AutoFillCreditCard);
// CONCATENATED MODULE: ./src/js/chromesettings/autofilladdress.js


class autofilladdress_AutoFillAddress extends chromesetting["a" /* default */] {
  constructor(storage) {
    super(chrome.privacy.services.autofillAddressEnabled); // bindings

    this.onChange = this.onChange.bind(this); // functions

    this.applySetting = this.createApplySetting(false, 'autofilladdress', 'block');
    this.clearSetting = this.createClearSetting('autofilladdress', 'unblock'); // init

    this.settingID = 'blockautofilladdress'; // If it exists, use value from old API

    if (storage.getItem('settings:blockautofill')) {
      this.settingDefault = false;
    } else {
      this.settingDefault = false;
    }
  }

  onChange(details) {
    this.setLevelOfControl(details.levelOfControl);
    this.setBlocked(details.value === false);
  }

}

/* harmony default export */ var autofilladdress = (autofilladdress_AutoFillAddress);
// EXTERNAL MODULE: ./src/js/firefoxsettings/chromesetting.js
var firefoxsettings_chromesetting = __webpack_require__(16);

// CONCATENATED MODULE: ./src/js/firefoxsettings/proxy.js




const proxy_pacengine = __webpack_require__(104);

class proxy_Proxy {
  constructor(app, foreground) {
    const handleProxyRequest = requestInfo => {
      const {
        origin
      } = new URL(requestInfo.url);
      const key = app.util.regionlist.getPort();
      const region = app.util.regionlist.getSelectedRegion();
      if (!region) return;
      const parseUrl = app.helpers.UrlParser.parse(origin);
      if (app.util.bypasslist.toArray().includes(origin) || app.util.bypasslist.toArray().includes(parseUrl.domain)) return {
        type: 'direct'
      }; //smart location proxy rule check

      const proxyRule = this.changeProxyRule(this.getUserRules(requestInfo.url));

      if (proxyRule) {
        return proxyRule;
      }

      return {
        host: region.host,
        port: region[key],
        type: region.scheme
      };
    };

    browser.proxy.onError.addListener(error => {
      debug(`Proxy error: ${error.message}`);
    });

    this.enabled = () => {
      return browser.proxy.onRequest.hasListener(handleProxyRequest);
    };

    this.getEnabled = () => {
      return browser.proxy.onRequest.hasListener(handleProxyRequest);
    };

    this.enable = async () => {
      if (this.enabled()) return;
      app.util.icon.online();
      app.util.storage.setItem('online', String(true));
      browser.proxy.onRequest.removeListener(handleProxyRequest);
      browser.proxy.onRequest.addListener(handleProxyRequest, {
        urls: ['<all_urls>']
      });
      http["a" /* default */].head('https://privateinternetaccess.com');
      Object(messagingFirefox["sendMessage"])(messagingFirefox["Target"].ALL, messagingFirefox["Type"].PROXY_ENABLE);
      const {
        util: {
          ipManager,
          settingsmanager
        }
      } = app;
      ipManager.update({
        retry: true
      });
      settingsmanager.clearAndReapplySettings('alwaysActive');
      return this;
    };

    this.disable = async () => {
      // if(!this.enabled()) return
      app.util.icon.offline();
      app.util.storage.setItem('online', String(false));
      browser.proxy.onRequest.removeListener(handleProxyRequest);
      Object(messagingFirefox["sendMessage"])(messagingFirefox["Target"].ALL, messagingFirefox["Type"].PROXY_DISABLE);
      const {
        util: {
          ipManager,
          settingsmanager
        }
      } = app;
      ipManager.update({
        retry: false
      });
      settingsmanager.clearAndReapplySettings('alwaysActive');
      return this;
    };

    this.userRulesProxy = null;
  }

  getUserRules(tab) {
    //get parse url and get smart proxy rule
    const {
      util: {
        icon
      },
      helpers
    } = app;
    const parseUrl = helpers.UrlParser.parse(tab);
    return icon.getCurrentState(tab, parseUrl);
  }

  changeProxyRule(tab) {
    const {
      util: {
        smartlocation,
        regionlist
      }
    } = app;
    const locations = Object.values(regionlist.getRegions());
    const key = app.util.regionlist.getPort();

    if (smartlocation.getSmartLocationRules('smartLocationRules').length > 0 && smartlocation.getSmartLocationRules('checkSmartLocation')) {
      // nodeDict is used for PAC script
      const nodeDict = proxy_pacengine.getNodeDictFromLocations(locations, key, [], true);

      if (nodeDict[tab.customCountry]) {
        //smart proxy rule
        const dnsname = nodeDict[tab.customCountry];
        const [host, port] = dnsname.split(':');
        return {
          type: 'https',
          host,
          port: Number(port) || 443
        };
      } else {
        return null;
      }
    } else {
      return null;
    }
  }

  isControllable() {
    return true;
  }

  getLevelOfControl() {
    return firefoxsettings_chromesetting["a" /* default */].controlled;
  }

  setLevelOfControl() {}

  static debug(msg, err) {
    return firefoxsettings_chromesetting["a" /* default */].debug('proxy', msg, err);
  }

}

/* harmony default export */ var firefoxsettings_proxy = (proxy_Proxy);
// EXTERNAL MODULE: ./src/js/firefoxsettings/webrtc.js
var firefoxsettings_webrtc = __webpack_require__(133);

// EXTERNAL MODULE: ./src/js/firefoxsettings/networkprediction.js
var firefoxsettings_networkprediction = __webpack_require__(136);

// EXTERNAL MODULE: ./src/js/firefoxsettings/httpreferer.js
var firefoxsettings_httpreferer = __webpack_require__(134);

// EXTERNAL MODULE: ./src/js/firefoxsettings/hyperlinkaudit.js
var firefoxsettings_hyperlinkaudit = __webpack_require__(135);

// EXTERNAL MODULE: ./src/js/firefoxsettings/trackingprotection.js
var trackingprotection = __webpack_require__(137);

// EXTERNAL MODULE: ./src/js/firefoxsettings/fingerprintprotection.js
var fingerprintprotection = __webpack_require__(138);

// EXTERNAL MODULE: ./src/js/helpers/applyListener.js
var applyListener = __webpack_require__(22);

// CONCATENATED MODULE: ./src/js/eventhandler/chrome/webrequest/onAuthRequired.js
/*
  *** WARNING ***
  This event handler is always active. It could be run while a direct connection is being
  used, while another proxy extension is active, or while the Private Internet Access
  extension is active.

  Being unaware of this could introduce serious bugs that compromise the security of the
  extension.

*/


function authenticate(app) {
  const active = details => {
    const {
      proxy,
      util: {
        regionlist
      }
    } = app;
    let proxyEnabled;
    proxyEnabled = proxy.enabled();
    const isValidHost = regionlist.testHost(details.challenger.host);
    const isValidPort = regionlist.testPort(details.challenger.port);
    const isActive = // proxyEnabled && 
    details.isProxy && isValidHost && isValidPort;
    debug('onauthrequired.js: testing if active');
    debug(`proxy enabled: ${proxyEnabled}`);
    debug(`isProxy: ${details.isProxy}`);
    debug(`challenger host: ${details.challenger.host}`);
    debug(`challenger port: ${details.challenger.port}`);
    debug(`possible hosts: ${JSON.stringify(regionlist.getPotentialHosts())}`);
    debug(`possible ports: ${JSON.stringify(regionlist.getPotentialPorts())}`);
    debug(`isActive: ${isActive}`);
    debug('onauthrequired.js: end test');
    return isActive;
  };

  return function handle(details) {
    try {
      debug('onauthrequired.js: servicing request for authentication');

      if (!active(details)) {
        return debug('onAuthRequired/1: refused.');
      }

      const {
        counter,
        user
      } = app.util;
      counter.inc(details.requestId);

      if (counter.get(details.requestId) > 1) {
        debug('onAuthRequired/1: failed.');
        counter.del(details.requestId);
        chrome.tabs.update({
          url: chrome.extension.getURL('html/errorpages/authfail.html')
        });
        user.logout();
        return {
          cancel: true
        };
      }

      if (user.getLoggedIn()) {
        debug('onAuthRequired/1: allowed.');
        const username = user.getUsername();
        const password = user.getPassword();
        const token = user.getAuthToken();
        let credentials = {
          cancel: true
        };

        if (username && password) {
          credentials = {
            authCredentials: {
              username,
              password
            }
          };
        } else if (token) {
          const tokenUser = token.substring(0, token.length / 2);
          const tokenPass = token.substring(token.length / 2);
          credentials = {
            authCredentials: {
              username: tokenUser,
              password: tokenPass
            }
          };
        }

        return credentials;
      }

      debug('onAuthRequired/1: user not logged in');
      user.logout();
      chrome.tabs.reload(details.tabId);
      return {
        cancel: true
      };
    } catch (err) {
      debug('onAuthRequired/1: refused due to error');
      debug(`error: ${JSON.stringify(err, Object.getOwnPropertyNames(err))}`);
      return {
        cancel: true
      };
    }
  };
}

/* harmony default export */ var onAuthRequired = (Object(applyListener["a" /* default */])((app, addListener) => {
  addListener(authenticate(app), {
    urls: ['<all_urls>']
  }, ['blocking']);
}));
// CONCATENATED MODULE: ./src/js/eventhandler/chrome/webrequest/onBeforeRedirect.js
/*
  *** WARNING ***
  This event handler is always active. It could be run while a direct connection is being
  used, while another proxy extension is active, or while the Private Internet Access
  extension is active.

  Being unaware of this could introduce serious bugs that compromise the security of the
  extension.

*/

/* harmony default export */ var onBeforeRedirect = (Object(applyListener["a" /* default */])((app, addListener) => {
  const {
    util: {
      httpsUpgrade
    }
  } = app;
  addListener(httpsUpgrade.onBeforeRedirect, {
    urls: ['https://*/*']
  });
}));
// CONCATENATED MODULE: ./src/js/eventhandler/chrome/webrequest/onBeforeRequest.js
/*
  *** WARNING ***
  This event handler is always active. It could be run while a direct connection is being
  used, while another proxy extension is active, or while the Private Internet Access
  extension is active.

  Being unaware of this could introduce serious bugs that compromise the security of the
  extension.

*/


function connFailRedirect(app) {
  const {
    util: {
      errorinfo
    }
  } = app;
  const connUrl = `chrome-extension://${chrome.runtime.id}/html/errorpages/connfail.html`;

  function isConnFailReload(url) {
    return connUrl === url.slice(0, connUrl.length) && url.slice(-7, url.length) === '#reload';
  }

  function getErrorUrl(errorID) {
    const url = errorinfo.get(errorID)[1];
    return url;
  }

  return details => {
    if (isConnFailReload(details.url)) {
      const url = new URL(details.url);
      const errorID = url.searchParams.get('id');
      const message = {
        id: errorID,
        request: 'RequestErrorDelete'
      };
      chrome.runtime.sendMessage(message);
      const redirectUrl = getErrorUrl(errorID);

      if (redirectUrl) {
        debug('connfail. try reload failed URL');
        return {
          redirectUrl
        };
      }
    }

    return undefined;
  };
}

function filterQueryParameters(app) {
  const {
    util: {
      settings
    }
  } = app;
  const filterLists = {
    blockutm: ['utm_source', 'utm_medium', 'utm_term', 'utm_content', 'utm_campaign'],
    blockfbclid: ['fbclid']
  };

  function containsFilterQueries(url, filterList) {
    return !!filterList.find(param => {
      return url.searchParams.has(param);
    });
  }

  function createFilteredUrl(url, filterList) {
    const copy = new URL(url);
    filterList.forEach(queryParam => {
      copy.searchParams.delete(queryParam);
    });
    return copy.toString();
  }

  function getFilterList() {
    return Object.keys(filterLists).filter(key => {
      return settings.isActive(key);
    }).map(key => {
      return filterLists[key];
    }).reduce((a, b) => {
      return [...a, ...b];
    }, []);
  }

  return details => {
    if (settings.enabled()) {
      const filterList = getFilterList();
      const url = new URL(details.url);

      if (filterList.length && containsFilterQueries(url, filterList)) {
        const redirectUrl = createFilteredUrl(url, filterList);

        if (redirectUrl) {
          debug(`onbeforerequest.js: filtered ${JSON.stringify(filterList)}`);
          return {
            redirectUrl
          };
        }

        debug(`onbeforerequest.js: failed to filter ${JSON.stringify(filterList)}`);
      }
    }

    return undefined;
  };
}

/* harmony default export */ var onBeforeRequest = (Object(applyListener["a" /* default */])((app, addListener) => {
  const {
    util: {
      httpsUpgrade
    }
  } = app;
  addListener(connFailRedirect(app), {
    urls: ['<all_urls>']
  }, ['blocking']);
  addListener(httpsUpgrade.onBeforeRequest, {
    urls: ['*://*/*', 'ftp://*/*']
  }, ['blocking']);
  addListener(filterQueryParameters(app), {
    urls: ['<all_urls>']
  }, ['blocking']);
}));
// CONCATENATED MODULE: ./src/js/eventhandler/chrome/webrequest/onCompleted.js
/*
  *** WARNING ***
  This event handler is always active. It could be run while a direct connection is being
  used, while another proxy extension is active, or while the Private Internet Access
  extension is active.

  Being unaware of this could introduce serious bugs that compromise the security of the
  extension.

*/


function onCompleted(app) {
  return details => {
    const {
      util: {
        counter
      }
    } = app;

    if (counter.get(details.requestId) >= 1) {
      counter.del(details.requestId);
    }
  };
}

/* harmony default export */ var webrequest_onCompleted = (Object(applyListener["a" /* default */])((app, addListener) => {
  const {
    util: {
      httpsUpgrade
    }
  } = app;
  chrome.webRequest.onCompleted.addListener(httpsUpgrade.onCompleted, {
    urls: ['*://*/*']
  });
  addListener(onCompleted(app), {
    urls: ['<all_urls>']
  });
}));
// CONCATENATED MODULE: ./src/js/eventhandler/chrome/webrequest/onErrorOccurred.js
/*
  *** WARNING ***
  This event handler is always active. It could be run while a direct connection is being
  used, while another proxy extension is active, or while the Private Internet Access
  extension is active.

  Being unaware of this could introduce serious bugs that compromise the security of the
  extension.

*/


function openErrorPage(app) {
  const networkErrors = ['net::ERR_CONNECTION_RESET', 'net::ERR_PROXY_CONNECTION_FAILED', 'net::ERR_CONNECTION_TIMED_OUT'];
  const tabQueries = [{
    active: true,
    status: 'loading',
    url: ['http://*/*', 'https://*/*']
  }, {
    active: true,
    status: 'complete',
    url: ['http://*/*', 'https://*/*']
  }];
  return details => {
    const connectedToPIA = app.proxy.enabled();
    const errorOnMainFrame = details.type === 'main_frame';
    const catchableError = networkErrors.indexOf(details.error) > -1;

    if (!connectedToPIA || !errorOnMainFrame || !catchableError) {
      return {
        cancel: false
      };
    }

    tabQueries.forEach(query => {
      chrome.tabs.query(query, tabs => {
        tabs.forEach(tab => {
          if (tab.id === details.tabId) {
            const errorID = app.util.errorinfo.set(details.error, details.url);
            const errorPageURL = chrome.extension.getURL(`html/errorpages/connfail.html?id=${errorID}`);
            chrome.tabs.update(tab.id, {
              url: errorPageURL
            });
          }
        });
      });
    });
    debug(`connection error: ${details.error}`);
    return {
      cancel: true
    };
  };
}

/* harmony default export */ var onErrorOccurred = (Object(applyListener["a" /* default */])((app, addListener) => {
  addListener(openErrorPage(app), {
    urls: ['<all_urls>']
  });
}));
// CONCATENATED MODULE: ./src/js/eventhandler/chrome/runtime/onInstalled.js


function newVersionNotification(app) {
  const isNewVersion = (newVersionStr, oldVersionStr) => {
    // TODO: potentially flawed (increase in # of digits doesn't necessarily mean a higher version)
    const oldVersion = parseInt(oldVersionStr.replace(/\./g, ''));
    const newVersion = parseInt(newVersionStr.replace(/\./g, ''));
    return newVersion > oldVersion;
  };

  const notify = async details => {
    await app.util.i18n.getWorker();
    const {
      contentsettings
    } = app;
    const title = t('ExtensionUpdated');
    const body = t('WelcomeToNewVersion');

    if (isNewVersion(app.buildinfo.version, details.previousVersion)) {
      contentsettings.extensionNotification.create(title, {
        body
      });
    }
  };

  return details => {
    if (details.reason === 'update') {
      notify(details);
    }
  };
}

/* harmony default export */ var onInstalled = (Object(applyListener["a" /* default */])((app, addListener) => {
  addListener(newVersionNotification(app));
}));
// CONCATENATED MODULE: ./src/js/eventhandler/chrome/runtime/onMessage.js
/*
  *** WARNING ***
  This event handler is always active. It could be run while a direct connection is being
  used, while another proxy extension is active, or while the Private Internet Access
  extension is active.

  Being unaware of this could introduce serious bugs that compromise the security of the
  extension.

*/


function initOnMessage(app) {
  return (msg, _sender, sendResponse) => {
    switch (msg.request) {
      case 'RequestErrorInfo':
        {
          const {
            errorinfo
          } = app.util;
          sendResponse(errorinfo.get(msg.id));
          break;
        }

      case 'RequestErrorDelete':
        {
          const {
            errorinfo
          } = app.util;
          errorinfo.delete(msg.id);
          break;
        }

      case 't':
        {
          const {
            i18n
          } = app.util;
          const m = i18n.t(msg.localeKey);
          sendResponse({
            m
          });
          break;
        }

      default:
        {
          break;
        }
    }
  };
}

/* harmony default export */ var onMessage = (Object(applyListener["a" /* default */])((app, addListener) => {
  addListener(initOnMessage(app));
}));
// CONCATENATED MODULE: ./src/js/eventhandler/chrome/runtime/onUpdateAvailable.js
/*
  *** WARNING ***
  This event handler is always active. It could be run while a direct connection is being
  used, while another proxy extension is active, or while the Private Internet Access
  extension is active.

  Being unaware of this could introduce serious bugs that compromise the security of the
  extension.

*/


function initReload(app) {
  return details => {
    const {
      proxy
    } = app;
    const {
      user
    } = app.util;

    if (user.inLocalStorage() || !user.getLoggedIn() && !proxy.enabled()) {
      chrome.runtime.reload();
    } else {
      debug(`onupdateavailable.js: v${details.version} will be installed when chrome restarts`);
    }
  };
}

/* harmony default export */ var onUpdateAvailable = (Object(applyListener["a" /* default */])((app, addListener) => {
  addListener(initReload(app));
}));
// CONCATENATED MODULE: ./src/js/eventhandler/chrome/cookies/onChanged.js
/*
  *** WARNING ***
  This event handler is always active. It could be run while a direct connection is being
  used, while another proxy extension is active, or while the Private Internet Access
  extension is active.

  Being unaware of this could introduce serious bugs that compromise the security of the
  extension.

*/

/* harmony default export */ var onChanged = (Object(applyListener["a" /* default */])((app, addListener) => {
  const {
    util: {
      httpsUpgrade
    }
  } = app;
  addListener(httpsUpgrade.onCookieChanged);
}));
// CONCATENATED MODULE: ./src/js/eventhandler/chrome/alarms/onAlarm.js
/*
  *** WARNING ***
  This event handler is always active. It could be run while a direct connection is being
  used, while another proxy extension is active, or while the Private Internet Access
  extension is active.

  Being unaware of this could introduce serious bugs that compromise the security of the
  extension.

*/


function initOnAlarm(app) {
  return function onAlarm(alarm) {
    switch (alarm.name) {
      case 'PollRegionList':
        app.util.regionlist.sync().then(() => {
          debug('onalarm.js: completed background poll of regions');
        }).catch(res => {
          debug(`onalarm.js: background poll of regions failed (${res.cause})`);
        });
        break;

      default:
        break;
    }
  };
}

/* harmony default export */ var onAlarm = (Object(applyListener["a" /* default */])((app, addListener) => {
  addListener(app.util.httpsUpgrade.onAlarm);
  addListener(initOnAlarm(app));
}));
// EXTERNAL MODULE: ./src/js/eventhandler/onError.js
var onError = __webpack_require__(106);

// CONCATENATED MODULE: ./src/js/eventhandler/eventhandler.js











/* harmony default export */ var eventhandler = (function (app) {
  const self = {};
  onAuthRequired(app, chrome.webRequest.onAuthRequired);
  onBeforeRedirect(app, chrome.webRequest.onBeforeRedirect);
  onBeforeRequest(app, chrome.webRequest.onBeforeRequest);
  webrequest_onCompleted(app, chrome.webRequest.onCompleted);
  onErrorOccurred(app, chrome.webRequest.onErrorOccurred);
  onInstalled(app, chrome.runtime.onInstalled);
  onMessage(app, chrome.runtime.onMessage);
  onUpdateAvailable(app, chrome.runtime.onUpdateAvailable);
  onChanged(app, chrome.cookies.onChanged);
  onAlarm(app, chrome.alarms.onAlarm);
  Object(onError["a" /* default */])(app, {
    addListener(listener) {
      window.addEventListener('error', listener);
    }

  });
  return self;
});
// CONCATENATED MODULE: ./src/js/core/courier/index.js
const FOREGROUND = 'foreground';
const BACKGROUND = 'background';

class Courier {
  constructor() {
    this.id = BACKGROUND;
    this.target = FOREGROUND;
    this.sendMesage = this.sendMessage.bind(this);
    this.receiveMessage = this.receiveMessage.bind(this); // handle listener

    if (typeof browser == 'undefined') {
      chrome.runtime.onMessage.addListener(this.receiveMessage);
    } else {
      browser.runtime.onMessage.addListener(this.receiveMessage);
    }
  }

  async sendMessage(type, data) {
    const msg = {
      type,
      target: this.target,
      data: data || {}
    };
    return chrome.runtime.sendMessage(msg);
  }

  receiveMessage(message, sender, response) {
    if (message.target !== this.id) {
      return false;
    }

    new Promise(resolve => {
      // do some work
      return resolve({
        data: 'message received on background'
      });
    }).then(response).catch(() => {
      return response(false);
    }); // must return true here to keep the response callback alive

    return true;
  }

}

/* harmony default export */ var courier = (Courier);
// CONCATENATED MODULE: ./src/js/core/network/index.js
class Network {
  constructor(app) {
    this.app = app;
    this.status = navigator.onLine;
    window.addEventListener('online', this.updateNetworkStatus);
    window.addEventListener('offline', this.updateNetworkStatus); // bindings

    this.updateNetworkStatus = this.updateNetworkStatus.bind(this);
  }

  async updateNetworkStatus() {
    // update local status
    this.status = navigator.onLine;

    if (typeof browser == 'undefined') {
      this.app.courier.sendMessage('refresh');
    } // check for region data


    const {
      regionlist
    } = this.app.util;

    if (!regionlist.hasRegions()) {
      // return here since sync will also call the latency tests
      return regionlist.sync();
    } // check to see if latency needs to updated
    // TODO: build a property into latencyManager to ensure to tests can't run at the same time


    const regions = regionlist.toArray();
    const pending = regions.some(region => {
      return region.latency === 'PENDING';
    });
    const {
      latencymanager
    } = this.app.util;

    if (pending) {
      await latencymanager.run();

      if (typeof browser == 'undefined') {
        this.app.courier.sendMessage('refresh');
      }
    }

    return Promise.resolve();
  }

}
// EXTERNAL MODULE: ./src/js/helpers/url-parser.js
var url_parser = __webpack_require__(139);

// CONCATENATED MODULE: ./src/js/background.js





































 // import Flash from '@contentsettings/flash';

























function isFrozen() {
  return true === true;
} // build background application (self)


const background_self = Object.create(null);
(async () => {
  // create util
  background_self.util = Object.create(null);
  background_self.helpers = Object.create(null); // setup storage (core dependency of application)

  if (typeof browser == "undefined") {
    background_self.util.storage = new util_storage(background_self);
    await background_self.util.storage.init();
  } else {
    background_self.util.storage = new firefoxsettings_storage["a" /* default */](background_self);
  } // event handling and basic browser info gathering


  background_self.frozen = isFrozen();
  background_self.buildinfo = new buildinfo["a" /* default */](background_self);
  background_self.logger = new logger["a" /* default */](background_self); // attach debugging to global scope

  window.debug = background_self.logger.debug; // attach other utility functions

  background_self.util.platforminfo = new platforminfo["a" /* default */](background_self);
  background_self.util.icon = new icon["a" /* default */](background_self);
  background_self.util.settings = new util_settings["a" /* default */](background_self);
  background_self.util.i18n = new util_i18n["a" /* default */](background_self);
  background_self.util.regionlist = new util_regionlist["a" /* default */](background_self);
  background_self.util.bypasslist = new util_bypasslist["a" /* default */](background_self);
  background_self.util.smartlocation = new smart_location["a" /* default */](background_self);
  background_self.util.counter = new counter["a" /* default */](background_self);
  background_self.util.user = new util_user["a" /* default */](background_self);
  background_self.util.latencymanager = new latencymanager["a" /* default */](background_self);
  background_self.util.regionsorter = new regionsorter["a" /* default */](background_self);
  background_self.util.settingsmanager = new util_settingsmanager["a" /* default */](background_self);
  background_self.util.errorinfo = new errorinfo["a" /* default */](background_self);
  background_self.util.httpsUpgrade = new util_https_upgrade(background_self);
  background_self.util.ipManager = new ipmanager["a" /* default */](background_self);
  background_self.util = Object.freeze(background_self.util);
  /* self.proxy is a %{browser}Setting like self.chromesettings.* objects are. */

  if (typeof browser == "undefined") {
    background_self.proxy = new chromesettings_proxy(background_self);
  } else {
    // message connection with foreground page
    background_self.adapter = new mockAppAdapter_MockAppAdapter(background_self);
    background_self.proxy = new firefoxsettings_proxy(background_self);
  } // setup event handler


  background_self.eventhandler = new eventhandler(background_self);
  background_self.contentsettings = Object.create(null);
  background_self.chromesettings = Object.create(null);

  if (typeof browser == "undefined") {
    // attach browser specific functions
    background_self.contentsettings.camera = new camera(background_self);
    background_self.contentsettings.microphone = new microphone(background_self);
    background_self.contentsettings.location = new contentsettings_location(background_self); // self.contentsettings.flash = new Flash(self);

    background_self.contentsettings.extensionNotification = new extension_notification(background_self); // attach chrome settings function

    background_self.chromesettings.networkprediction = new networkprediction();
    background_self.chromesettings.httpreferer = new httpreferer();
    background_self.chromesettings.hyperlinkaudit = new hyperlinkaudit();
    background_self.chromesettings.webrtc = new webrtc();
    background_self.chromesettings.thirdpartycookies = new thirdpartycookies();
    background_self.chromesettings.safebrowsing = new safebrowsing(); // new API starting w/ chrome 70

    background_self.chromesettings.autofillcreditcard = new autofillcreditcard(background_self.util.storage);
    background_self.chromesettings.autofilladdress = new autofilladdress(background_self.util.storage); // old API, remove after chrome 70 reaches general availability

    background_self.chromesettings.autofill = new autofill();
  } else {
    background_self.chromesettings = Object.create(null);
    background_self.chromesettings.webrtc = new firefoxsettings_webrtc["a" /* default */](background_self);
    background_self.chromesettings.networkprediction = new firefoxsettings_networkprediction["a" /* default */](background_self);
    background_self.chromesettings.httpreferer = new firefoxsettings_httpreferer["a" /* default */](background_self);
    background_self.chromesettings.hyperlinkaudit = new firefoxsettings_hyperlinkaudit["a" /* default */](background_self);
    background_self.chromesettings.trackingprotection = new trackingprotection["a" /* default */](background_self);
    background_self.chromesettings.fingerprintprotection = new fingerprintprotection["a" /* default */](background_self);
  }

  background_self.sameApp = new js_sameApp["a" /* default */](background_self); // Initialize all functions

  const initSettings = async settings => {
    const pending = Object.values(settings).filter(setting => {
      return setting.init;
    }).map(setting => {
      return setting.init();
    });
    await Promise.all(pending);
  };

  await initSettings(background_self.chromesettings);
  await initSettings(background_self.contentsettings); // only initialize settings AFTER intializing chrome/content settings

  background_self.util.settings.init(); // only initialize bypasslist AFTER settings

  background_self.util.bypasslist.init();
  background_self.util.smartlocation.init(); // setup courier & network

  background_self.courier = new courier();
  background_self.network = new Network(background_self); // trigger regionlist sync

  const {
    regionlist
  } = background_self.util;
  regionlist.sync(); //Smart location on tab change

  background_self.helpers.UrlParser = new url_parser["a" /* default */](); //when a tab is updated

  chrome.tabs.onUpdated.addListener(tabId => {
    background_self.util.icon.upatedOnChangeTab(tabId);
  });
  chrome.windows.onCreated.addListener(function () {
    background_self.util.user.checkUserName();
  }); //When tabs are changed

  chrome.tabs.onActivated.addListener(activeInfo => {
    background_self.util.icon.upatedOnChangeTab(activeInfo.tabId);
  }); // attach app to window

  window.app = Object.freeze(background_self);
  debug('background.js: mounted to window successfully');
  const {
    proxy,
    sameApp,
    util: {
      storage,
      user,
      ipManager
    }
  } = background_self;
  await user.init();

  if (typeof browser == "undefined") {
    await proxy.init();
    await proxy.readSettings();
  }

  await sameApp.init();
  const loggedIn = user.getLoggedIn().length > 0 ? JSON.parse(user.getLoggedIn()) : user.getLoggedIn();

  if (loggedIn && JSON.parse(storage.getItem('online')) && proxy.isControllable()) {
    await proxy.enable();
  } else {
    await proxy.disable(); // trigger ip update

    ipManager.update({
      retry: true
    });
  }

  debug('background.js: initialized successfully');
})().catch(async err => {
  if (debug) {
    debug('background.js: failed to initialize');
    debug(err);
  }

  if (background_self.proxy) {
    await background_self.proxy.disable();
  }
});

/***/ })
/******/ ]);
//# sourceMappingURL=background.js.map