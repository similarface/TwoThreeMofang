/* ========================================================================
 * author:  bomee
 * version: 1.4.3
 * ======================================================================== */
$(function() {
  /**
   * 覆盖默认的弹出框.
   */
  var tip = window.alert = function(text, delay) {
    var $alert = $('<div id="global_alert" class="alert alert-danger alert-dismissible fade in" role="alert" title="点击关闭"><strong> ' + text + '</strong></div>')
      .one('click', function() {
        $(this).alert('close');
      })
      .appendTo('body');

    window.setTimeout(function() {
      $alert.alert('close');
      $alert = null;
      delete $alert;
    }, delay || 3000);
  };

  $.ajaxSetup({
    cache: false
  });

  /**
   * like $.getJSON, Load JSON-encoded data from the server using a POST HTTP
   * request.
   */
  $.postJSON = function(url, data, fnSuccess, fnError) {
    $.ajax({
      url: url,
      type: "POST",
      dataType: "json",
      cache: false,
      contentType: "application/json",
      data: JSON.stringify(data),
      success: function(result) {
        fnSuccess && (fnSuccess(result) || 1) || (typeof result.code != 'undefined' && !result.code && tip(result.error || '更新失败...'));
      },
      error: function(err) {
        if (err.status == 401) {
          return tip(err.status + ' ' + err.statusText + ', 当前会话已失效，请去新窗口 <a target="_blank" href="/login?from=' + encodeURIComponent(location.href) + '">登陆</a> 后继续操作!', 60000);
        }
        fnError && (fnError.apply($, Array.prototype.slice.call(arguments)) || 1) || tip(err.status + ' ' + err.statusText);
      }
    });
  };

  /**
   * jQuery dataTable 默认值
   */
  $.fn.dataTable.defaults.column.sDefaultContent = '';
  $.extend($.fn.dataTable.defaults, {
    "pageLength": 15,
    "bLengthChange": false,
    "ordering": false,
    "processing": true,
    "serverSide": true,
    "searching": false,
    /*"stateSave": true,*/
    "language": {
      "lengthMenu": "每页显示 _MENU_ 记录",
      "zeroRecords": "当前数据结果为空",
      "emptyTable": "当前数据结果为空",
      "info": "第 _PAGE_ / _PAGES_ 页 共  _TOTAL_ 条记录",
      "infoFiltered": "(筛选自 _MAX_ 条记录)",
      "infoEmpty": "共  0 条记录",
      "loadingRecords": "Please wait - loading...",
      "processing": "Please wait - loading..."
    },
    "classes": {
      "sProcessing": " dataTables_processing "
    }
  });

  /**
   * jQuery dataTable 扩展
   */
  $.fn.dataTable.pagerAjax = function(opts) {
    return function(request, drawCallback, settings) {
      settings.jqXHR = $.ajax({
        "type": "POST",
        "url": opts.url,
        "data": JSON.stringify({
          "offset": request.start,
          "length": request.length,
          "search": $.isPlainObject(request.search.value) || $.isArray(request.search.value) ? request.search.value : null
        }),
        "contentType": "application/json",
        "dataType": "json",
        "cache": false,
        "success": function(json) {
          $(settings.nTable).trigger('xhr.dt', [settings, json]);
          drawCallback({
            "draw": request.draw,
            "recordsTotal": json.recordsTotal,
            "recordsFiltered": json.recordsTotal,
            "data": json.data
          });
        },
        "error": function() {
          drawCallback({
            "draw": request.draw,
            "recordsTotal": 0,
            "recordsFiltered": 0,
            "data": []
          });
        }
      });
    }
  };

  /**
   * jQuery dataTable 重绘当前数据
   */
  $.fn.dataTable.Api.register('redraw()', function() {
    return this.iterator('table', function(settings) {
      settings.bAjaxDataGet = false;
      settings.aiDisplay = settings.aiDisplayMaster.slice();
      $.fn.dataTable.ext.internal._fnDraw(settings);
      settings.bAjaxDataGet = true;
    });
  });

  /**
   * jQuery dataTable 插入行, 索引为0
   */
  $.fn.dataTable.Api.register('row.insert()', function(row) {
    if (row instanceof $ && row.length) {
      row = row[0];
    }
    var rows = this.iterator('table', function(settings) {
      if (row.nodeName && row.nodeName.toUpperCase() === 'TR') {
        throw Error('not support insert html');
      }
      var nTr = false;
      var oData = $.extend(true, {}, $.fn.dataTable.models.oRow, {
        src: nTr ? 'dom' : 'data'
      });

      oData._aData = row;
      settings.aoData.unshift(oData);
      settings.aiDisplayMaster.push(settings.aoData.length - 1);
      return 0;
    });

    return this.row(rows[0]);
  });

  /**
   * jQuery dataTable 扩展查询
   */
  $.fn.dataTable.Api.register('searchEx()', function(input, regex, smart, caseInsen) {
    var ctx = this.context;

    if (input === undefined) {
      // get
      return ctx.length !== 0 ? ctx[0].oPreviousSearch.sSearch : undefined;
    }

    // set
    return this.iterator('table', function(settings) {
      $.fn.dataTable.ext.internal._fnFilterComplete(settings, $.extend({}, settings.oPreviousSearch, {
        "sSearch": input,
        "bRegex": regex === null ? false : regex,
        "bSmart": smart === null ? true : smart,
        "bCaseInsensitive": caseInsen === null ? true : caseInsen
      }), 1);
    });
  });

  /**
   * 内部私有方法
   */
  var _fnObjectGetPropertyChainValue = function(obj, propertyChain) {
      /* 获取属性链的值 */
      if (!obj) return;
      if (!propertyChain) return obj;
      var property,
        chains = propertyChain.split('.'),
        i = 0,
        len = chains.length;
      for (;
        (property = chains[i]) && i < len - 1; i++) {
        if (!obj[property]) return;
        obj = obj[property];
      }
      return obj[property];
    },
    _fnObjectSetPropertyChainValue = function(obj, propertyChain, value, allowMulti) {
      /* 设置属性链的值 */
      if (!obj || !propertyChain) return;
      var property,
        chainObj = obj,
        chains = propertyChain.split('.'),
        i = 0,
        len = chains.length;
      for (;
        (property = chains[i]) && i < len - 1; i++) {
        if (!chainObj[property]) {
          chainObj[property] = {};
        }
        chainObj = chainObj[property];
      }
      // 改进版：checkbox的多选可以组合为数组
      if (!allowMulti || chainObj[property] === undefined) {
        chainObj[property] = value;
      } else {
        var pv = chainObj[property];
        if ($.isArray(pv)) {
          pv.push(value);
        } else {
          chainObj[property] = [pv, value];
        }
      }
      return obj;
    };

  /**
   * jQuery form 扩展获取数据
   */
  $.fn.formGet = function(opts) {
    opts = $.extend({}, opts);
    var data = {},
      els = opts.formGroup ? this.find('[form-group="' + opts.formGroup + '"]') : this.find('[name]');
    if (!els || !els.length) {
      return data;
    }

    var fnSetValue = (function(emptyToNull) {
      return emptyToNull ? function(obj, propertyChain, value, allowMulti) {
        value !== '' && _fnObjectSetPropertyChainValue(obj, propertyChain, value, allowMulti)
      } : _fnObjectSetPropertyChainValue
    })(opts.emptyToNull);

    els.each(function() {
      var $this = $(this),
        type = $this.attr('type'),
        name = $this.attr('name'), // 可能为属性链
        tag = this.tagName.toLowerCase();
      if (tag == 'input') {
        if (type == 'checkbox') {
          var v = $(this).val();
          if (v == 'on' || !v) {
            fnSetValue(data, name, $(this).prop('checked'));
          } else {
            $(this).prop('checked') && fnSetValue(data, name, v, true);
          }
        } else if (type == 'radio') {
          this.checked && fnSetValue(data, name, $this.val());
        } else {
          fnSetValue(data, name, $this.val());
        }
      } else if ('|select|textarea|'.indexOf('|' + tag + '|') > -1) {
        fnSetValue(data, name, $this.val());
      } else {
        fnSetValue(data, name, $.trim($this.text()));
      }
    });
    return data;
  };

  /**
   * jQuery form 扩展绑定数据
   * 
   */
  $.fn.formSet = function(data, formGroup) {
    var els = formGroup ? this.find('[form-group="' + formGroup + '"]') : this.find('[name]');
    if (!els || !els.length) {
      return this;
    }

    els.each(function() {
      var $this = $(this),
        type = $this.attr('type'),
        name = $this.attr('name'),
        tag = this.tagName.toLowerCase();

      var value = _fnObjectGetPropertyChainValue(data, name);
      if (tag == 'input') {
        if (type == 'checkbox') {
          var v = $(this).val();
          if (v == 'on' || !v) {
            this.checked = value ? 'checked' : '';
          } else {
            this.checked = $.isArray(value) && value.indexOf(v) > -1 ? 'checked' : ''
          }
        } else if (type == 'radio') {
          this.checked = $this.val() == String(value) ? 'checked' : '';
        } else {
          $this.val(value);
        }
      } else if ('|select|textarea|'.indexOf('|' + tag + '|') > -1) {
        $this.val(value);
      } else {
        $this.html(value);
      }
    });
    return this;
  };

  /**
   * 模态框点击背景的默认行为
   */
  $.fn.modal.Constructor.DEFAULTS.backdrop = 'static';
  /**
   * 通用的修改更新模块，保存操作使用事件：save.bs.modal 简化编辑与展示的数据同步问题
   */
  $.fn.modal.Constructor.prototype.beginEdit = function(arg) {
    var callback, ctx;
    if ($.isPlainObject(arg)) {
      callback = arg.callback, ctx = arg.context;
    } else {
      ctx = arg;
    }
    var $ele = this.$element;
    if (!$ele.data('beginEdit')) {
      $ele.data('beginEdit', true); // 避免重复订阅
      $ele.on('click.save.bs.modal', '[modal-button="save"]', function() {
          $(this).button('loading');
          $ele.trigger($.Event('save.bs.modal', {}));
        })
        .on('hidden.bs.modal', function() {
          $(this).find('button[modal-button="save"]').button('reset');
        });
    }
    if (ctx) {
      var $ctx = $(ctx);
      $ele.data('beginEdit-ctx', $ctx);
      $ele.find('[ref-selector]').each(function() {
        var selector = $(this).attr('ref-selector');
        var attr, offset;
        if ((offset = selector.indexOf('[')) > 0) {
          attr = selector.slice(offset + 1, -1);
        }

        var value = attr ? $ctx.find(selector).attr(attr) : $.trim($ctx.find(selector).text());

        if (callback && callback(this, value) === false) return;

        if ($(this).is('[type="radio"]')) {
          (this.checked = $(this).val() == value) && $(this).trigger('change');
        } else {
          $(this).val(value);
        }
      });
    }
    this.show();
  };

  $.fn.modal.Constructor.prototype.endEdit = function(arg) {
    var callback, keepShow;
    if ($.isPlainObject(arg)) {
      callback = arg.callback, keepShow = arg.show;
    } else {
      $.isFunction(arg) ? (callback = arg, keepShow = false) : keepShow = arg;
    }
    if (keepShow) {
      this.$element.find('button[modal-button="save"]').button('reset');
      return;
    }

    var $ele = this.$element,
      $ctx;
    if ($ele.data('beginEdit-ctx')) {
      var $ctx = $ele.data('beginEdit-ctx');
      $ele.find('[ref-selector]').each(function() {
        var selector = $(this).attr('ref-selector');
        var attr, offset;
        if ((offset = selector.indexOf('[')) > 0) {
          attr = selector.slice(offset + 1, -1);
        }
        if ($(this).is('[type="radio"]') && !this.checked) {
          return;
        }

        var $selector = $ctx.find(selector);
        if (callback && callback(this, $selector) === false) return;

        attr ? $selector.attr(attr, $(this).val()) : $selector.html($(this).val());
      });
      $ele.data('beginEdit-ctx', null);
    }
    this.hide();
  };


  /**
   * 格式化字符串 第一个参数为格式化模板 format('this is a {0} template!', 'format');
   * format('this is a {0.message} template!', { message: 'format'}); 等同于
   * format('this is a {message} template!', { message: 'format' });
   */
  $.format = function() {
    var template = arguments[0],
      templateArgs = arguments,
      stringify = function(obj) {
        if (obj == null) {
          return '';
        } else if (typeof obj === 'function') {
          return obj();
        } else if (typeof obj !== 'string') {
          return JSON.stringify ? JSON.stringify(obj) : obj;
        }
        return obj;
      };
    return template.replace(/\{\w+(\.\w+)*\}/g, function(match) {
      var propChains = match.slice(1, -1).split('.');
      var index = isNaN(propChains[0]) ? 0 : +propChains.shift();
      var arg, prop;
      if (index + 1 < templateArgs.length) {
        arg = templateArgs[index + 1];
        while (prop = propChains.shift()) {
          arg = arg[prop];
        }
        return stringify(arg);
      }
      return match;
    });
  };
  
  /**
   * 格式化日期
   */
  $.formatDate = function(date){
    if(typeof date === 'number'){
      var d;
      date = (d = new Date(), d.setTime(date), d);
    }
    
    var fixedZero = function(v){
        return ('00' + v).slice(-2);
    };
    
    return [date.getFullYear(), '-', fixedZero(date.getMonth() + 1), '-', fixedZero(date.getDate()), ' ', fixedZero(date.getHours()), ':', fixedZero(date.getMinutes()), ':', fixedZero(date.getSeconds())].join('');
  };
  /**
   * 解析日期
   */
  $.parseDate = function (dateStr) {
    var d = null;
    var matches = /^\s*([12]\d{3}|\d{2})[-\/\u5E74](1[0-2]|0?[1-9])[-\/\u6708]([12]\d|3[01]|0?[1-9])\u65E5?(?: (1\d|2[0-3]|0?[0-9])[:\u65F6]([1-5]\d|0?\d)[:\u5206]?([1-5]\d|0?\d)?)?/.exec(dateStr);
    if (matches == null) {
      throw new Error("\u65E0\u6548\u7684\u65E5\u671F\u683C\u5F0F");
    }
    d = new Date(matches[1], Number(matches[2]) - 1, matches[3]);
    if(matches[4] != null) {
      d.setHours(+matches[4]);
    } 
    if(matches[5] != null) {
      d.setMinutes(+matches[5]);
    }
    if(matches[6] != null) {
      d.setSeconds(+matches[6]);
    }
    return d;
  };
  

  /**
   * 高级版join, 数组对象可以为复杂对象
   */
  $.join = function(arr, joint, prop) {
    if (arr == null) return '';
    if (prop == null) return arr.join(joint);
    joint = joint || ',';
    var i = 0,
      item, resultArr = [];
    for (; item = arr[i]; i++) {
      resultArr[i] = item[prop];
    }
    return resultArr.join(joint);
  };

  (function autoActiveMenuItem() {
    /**
     * 初始左侧菜单
     */
    $('#side-menu').metisMenu({
      toggle: false
    });
    
    /**
     * 根据url高亮左边菜单项
     */
    var url = window.location, $a, $parentA;
    $('ul.nav a').each(function() {
      if(this.href === url.href) {
          $a = $(this);
          return false; // 最佳匹配直接break;
      }
      
      if(new RegExp('^' + this.href + '(/|#|\\?)').test(url.href)){
          $a = $(this); // 可能匹配
      }
    });
    
    if($a){
      $parentA = $a.addClass('active').closest('ul.nav').addClass('in').prev(); // 父级a标签
      $a.length && (window.document.title = $parentA.length ? $parentA.text().trim() + '-' + $a.text().trim() : $a.text().trim());
      $parentA.parent('li').addClass('active');
    }

    /**
     * 根据hash选中tab
     */
    if (url.hash) {
      $('a[data-toggle="tab"][href="' + url.hash + '"]').tab('show');
    }
  })();

/*  
 * 2015-11-13移除bootstrap3-wysihtml5的文本编辑框
 * $.fn.wysihtml5 && (function() {
    $('textarea.textarea').wysihtml5({
      "size": "sm",
      "useLineBreaks": false,
      "stylesheets": ["/plugins/bootstrap3-wysihtml5/wysihtml5-stylesheet.css"],
      "toolbar": {
        "color": true,
        "blockquote": false,
        "fa": true,
        "html": true,
        "paragraph": true
      },
      "customTemplates": {
        paragraph: function(context) {
          return '<li><div class="btn-group"><a class="btn btn-sm btn-default" data-wysihtml5-command="formatInline" data-wysihtml5-command-value="p" title="插入段落" tabindex="-1" href="javascript:;" unselectable="on"><span class="fa fa-paragraph"></span></a></div></li>';
        }
      }
    });
  })();*/
  
  //初始化文本编辑器
  $(".ueditorFlag").each(function() {
	  var id = this.id;	
	  var ue = UE.getEditor(id, {
	      pasteplain: true /*纯文本粘贴*/
	  });	
  	console.log('ueditor for ' + id + ' init.');
  });
  
  

  $('input[format-barcode]').keypress(function(evt) {
    evt = evt || window.event;
    var charCode = evt.which || evt.charCode;
    var keyCode = evt.keyCode;

    if (keyCode == 8 || keyCode == 46 || (charCode == 118 && evt.ctrlKey)) {
      return keyCode != charCode; /* 因为数字键盘的小数点很特殊 */
    }

    if (charCode != 45 && (charCode < 48 || charCode > 59)) {
      return false;
    }

    if (charCode != 45 && (evt.target.value.length == 3 || evt.target.value.length == 8)) {
      evt.target.value += '-';
    }
  });
});


var ModalDialog = function(html) {
  var $dialog = $(html);
  this.show = function(message) {
    $dialog.find('.message').text(message);
    $dialog.modal();
  };
  this.hide = function() {
    $dialog.modal('hide');
  };
};


/**
 * loading dialog
 */
var loadingDialog = new ModalDialog(
  '<div class="modal fade" data-backdrop="static" data-keyboard="false" tabindex="-1" role="dialog" aria-hidden="true" style="padding-top:15%; overflow-y:visible;">' +
  '<div class="modal-dialog modal-sm">' +
  '<div class="modal-content">' +
  '<div class="modal-header"><h4 style="margin:0;" class="message"></h4></div>' +
  '<div class="modal-body">' +
  '<div class="progress progress-striped active" style="margin-bottom:0;"><div class="progress-bar" style="width: 100%"></div></div>' +
  '</div>' +
  '</div></div></div>');

/**
 * alert dialog
 */
var alertDialog = new ModalDialog(
  '<div class="modal fade" data-backdrop="true" data-keyboard="false" tabindex="-1" role="dialog" aria-hidden="true" style="padding-top:15%; overflow-y:visible;">' +
  '<div class="modal-dialog modal-sm">' +
  '<div class="modal-content">' +
  '<div class="modal-header"><h4 style="margin:0;" class="text-center">提示</h4></div>' +
  '<div class="modal-body">' +
  '<div class="message"></div>' +
  '</div>' +
  '<div class="modal-footer" style="text-align: center; padding-top:5px;padding-bottom:5px;"><button type="button" class="btn btn-primary btn-xs" data-dismiss="modal">&emsp;确定&emsp;</button></div>' +
  '</div></div></div>');

var MF = {
  toGenderString: function(gender) {
    return gender == '0' ? '全部' : (gender == '1' ? '男' : '女');
  },
  format: $.format,
  Dialog:{
    alert: function(msg){ alertDialog.show(msg);},
    loading: function(msg){ loadingDialog.show(msgm || 'Loading...');},
    hideLoading: function(){ loadingDialog.hide();}
  },
  Config: {
    validate: function(cfg) {
      return $.extend({
        errorClass: "has-error",
        focusCleanup: true,
        focusInvalid: false,
        errorPlacement: function() {},
        highlight: function(element, errorClass) {
          $(element).closest('.form-group').addClass(errorClass);
        },
        unhighlight: function(element, errorClass) {
          var $fg = $(element).closest('.form-group');
          if ($fg.hasClass(errorClass)) {
            $(element).tooltip('hide');
          }
          $fg.removeClass(errorClass);
        },
        showErrors: function(errorMap, errorList) {
          for (var i = 0, item; item = errorList[i]; i++) {
            $(item.element).attr('data-original-title', item.message).tooltip({
              trigger: 'manual',
              placement: 'bottom',
              template: '<div class="tooltip error" role="tooltip"><div class="tooltip-arrow"></div><div class="tooltip-inner"></div></div>'
            }).tooltip('show');
          }
          this.defaultShowErrors();
        }
      }, cfg);
    }
  }
};
