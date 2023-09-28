from django.db import models
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.models import Image

from geomanager.blocks import (
    InlineLegendBlock,
    LayerMoreInfoBlock,
    QueryParamSelectableBlock,
    QueryParamStaticBlock
)
from geomanager.models.core import Dataset, BaseLayer


class TmsLayer(TimeStampedModel, ClusterableModel, BaseLayer):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name="tms_layers", verbose_name=_("dataset"))
    base_url = models.CharField(max_length=500, verbose_name=_("Base url for TMS"), )

    query_params_static = StreamField([
        ('param', QueryParamStaticBlock(label=_("Query Parameter")))
    ], use_json_field=True, null=True, blank=True, verbose_name=_("Static Query Params"),
        help_text=_("Static query params to be added to the url"))

    query_params_selectable = StreamField([
        ('param', QueryParamSelectableBlock(label=_("Selectable Query Parameter")))
    ], use_json_field=True, null=True, blank=True, verbose_name=_("Query Params With selectable Options"),
        help_text=_("This should provide a list of options that users "
                    "can choose to change the query parameter of the url"))

    params_selectors_side_by_side = models.BooleanField(default=False,
                                                        verbose_name=_("Arrange Param Selectors side by side"))

    legend = StreamField([
        ('legend', InlineLegendBlock(label=_("Custom Legend")),),
        ('legend_image', ImageChooserBlock(label=_("Custom Image")),),
    ], use_json_field=True, null=True, blank=True, max_num=1, verbose_name=_("Legend"), )

    more_info = StreamField([
        ('more_info', LayerMoreInfoBlock(label=_("Info link")),),
    ], block_counts={
        'more_info': {'max_num': 1},
    }, use_json_field=True, null=True, blank=True, max_num=1, verbose_name=_("More Info"), )

    panels = [
        FieldPanel("dataset"),
        FieldPanel("title"),
        FieldPanel("default"),
        FieldPanel("base_url"),
        FieldPanel("query_params_static"),
        FieldPanel("query_params_selectable"),
        FieldPanel("params_selectors_side_by_side"),
        FieldPanel("legend"),
        FieldPanel("more_info"),
    ]

    def __str__(self):
        return self.title

    @property
    def layer_config(self):
        tms_url = self.base_url

        query_params = {}

        if self.dataset.multi_temporal:
            query_params.update({
                "time": "{{time}}"
            })

        static_params = self.get_static_params()
        if static_params:
            query_params.update(static_params)

        query_str = '&'.join([f"{key}={value}" for key, value in query_params.items()])

        if query_str:
            tms_url = f"{tms_url}?{query_str}"

        layer_config = {
            "type": "raster",
            "source": {
                "type": "raster",
                "tiles": [tms_url]
            }
        }

        return layer_config

    def get_selectable_params(self):
        params = {}
        if self.query_params_selectable:
            for query_param in self.query_params_selectable:
                data = query_param.block.get_api_representation(query_param.value)
                val = f"{data.get('name')}"
                params.update({val: data})
        return params

    def get_static_params(self):
        params = {}
        if self.query_params_static:
            for query_param in self.query_params_static:
                data = query_param.block.get_api_representation(query_param.value)
                val = f"{data.get('key')}"
                params.update({val: data.get('value')})
        return params

    def get_selectable_params_config(self):
        selectable_params = self.get_selectable_params()
        config = []

        for key, param_config in selectable_params.items():
            param_config = {
                "key": key,
                "required": True,
                "type": param_config.get("type"),
                "options": param_config.get("options"),
                "sentence": f"{param_config.get('label') or key} {{selector}}",
            }

            config.append(param_config)

        return config

    @property
    def params(self):
        params = {}
        if self.dataset.multi_temporal:
            params.update({"time": ""})

        selector_config = self.get_selectable_params_config()

        for selector_param in selector_config:
            default = None
            for option in selector_param.get("options"):
                if option.get("default"):
                    default = option.get("value")
                    break
            if not default:
                default = selector_param.get("options")[0].get("value")
            params.update({selector_param.get("key"): default})

        return params

    @property
    def param_selector_config(self):
        config = []

        if self.dataset.multi_temporal:
            time_config = {
                "key": "time",
                "required": True,
                "sentence": "{selector}",
                "type": "datetime",
                "availableDates": [],
            }

            time_config.update({
                "dateFormat": {"currentTime": "yyyy-mm-dd HH:MM"},
            })

            config.append(time_config)
        selectable_params_config = self.get_selectable_params_config()

        config.extend(selectable_params_config)

        return config

    def get_legend_config(self, request):

        # default config
        config = {
            "type": "basic",
            "items": []
        }

        legend_block = self.legend

        # only one legend block entry is expected
        if legend_block:
            legend_block = legend_block[0]

        if legend_block:
            if isinstance(legend_block.value, Image):
                image_url = legend_block.value.file.url
                if request:
                    image_url = request.build_absolute_uri(image_url)
                config.update({"type": "image", "imageUrl": image_url})
                return config

            data = legend_block.block.get_api_representation(legend_block.value)

            config.update({"type": data.get("type")})

            for item in data.get("items"):
                config["items"].append({
                    "name": item.get("value"),
                    "color": item.get("color")
                })

        return config
