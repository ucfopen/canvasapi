from canvasapi.canvas_object import CanvasObject
from canvasapi.exceptions import RequiredFieldMissing
from canvasapi.paginated_list import PaginatedList
from canvasapi.util import combine_kwargs, obj_or_id


class Module(CanvasObject):
    def __str__(self):
        return "{} ({})".format(self.name, self.id)

    def edit(self, **kwargs):
        """
        Update this module.

        :calls: `PUT /api/v1/courses/:course_id/modules/:id \
        <https://canvas.instructure.com/doc/api/modules.html#method.context_modules_api.update>`_

        :rtype: :class:`canvasapi.module.Module`
        """
        response = self._requester.request(
            "PUT",
            "courses/{}/modules/{}".format(self.course_id, self.id),
            _kwargs=combine_kwargs(**kwargs),
        )
        module_json = response.json()
        module_json.update({"course_id": self.course_id})

        return Module(self._requester, module_json)

    def delete(self):
        """
        Delete this module.

        :calls: `DELETE /api/v1/courses/:course_id/modules/:id \
        <https://canvas.instructure.com/doc/api/modules.html#method.context_modules_api.destroy>`_

        :rtype: :class:`canvasapi.module.Module`
        """
        response = self._requester.request(
            "DELETE", "courses/{}/modules/{}".format(self.course_id, self.id)
        )
        module_json = response.json()
        module_json.update({"course_id": self.course_id})

        return Module(self._requester, module_json)

    def relock(self):
        """
        Reset module progressions to their default locked state and recalculates
        them based on the current requirements.

        Adding progression requirements to an active course will not lock students
        out of modules they have already unlocked unless this action is called.

        :calls: `PUT /api/v1/courses/:course_id/modules/:id/relock \
        <https://canvas.instructure.com/doc/api/modules.html#method.context_modules_api.relock>`_

        :rtype: :class:`canvasapi.module.Module`
        """
        response = self._requester.request(
            "PUT", "courses/{}/modules/{}/relock".format(self.course_id, self.id)
        )
        module_json = response.json()
        module_json.update({"course_id": self.course_id})

        return Module(self._requester, module_json)

    def get_module_items(self, **kwargs):
        """
        List all of the items in this module.

        :calls: `GET /api/v1/courses/:course_id/modules/:module_id/items \
        <https://canvas.instructure.com/doc/api/modules.html#method.context_module_items_api.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.module.ModuleItem`
        """
        return PaginatedList(
            ModuleItem,
            self._requester,
            "GET",
            "courses/{}/modules/{}/items".format(self.course_id, self.id),
            {"course_id": self.course_id},
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_module_item(self, module_item, **kwargs):
        """
        Retrieve a module item by ID.

        :calls: `GET /api/v1/courses/:course_id/modules/:module_id/items/:id \
        <https://canvas.instructure.com/doc/api/modules.html#method.context_module_items_api.show>`_

        :param module_item: The object or ID of the module item.
        :type module_item: :class:`canvasapi.module.ModuleItem` or dict

        :rtype: :class:`canvasapi.module.ModuleItem`
        """
        module_item_id = obj_or_id(module_item, "module_item", (ModuleItem,))

        response = self._requester.request(
            "GET",
            "courses/{}/modules/{}/items/{}".format(
                self.course_id, self.id, module_item_id
            ),
            _kwargs=combine_kwargs(**kwargs),
        )
        module_item_json = response.json()
        module_item_json.update({"course_id": self.course_id})

        return ModuleItem(self._requester, module_item_json)

    def create_module_item(self, module_item, **kwargs):
        """
        Create a module item.

        :calls: `POST /api/v1/courses/:course_id/modules/:module_id/items \
        <https://canvas.instructure.com/doc/api/modules.html#method.context_module_items_api.create>`_

        :param module_item: The attributes to create the module item with.
        :type module_item: dict
        :returns: The created module item.
        :rtype: :class:`canvasapi.module.ModuleItem`
        """

        unrequired_types = ["ExternalUrl", "Page", "SubHeader"]

        if isinstance(module_item, dict) and "type" in module_item:
            # content_id is not required for unrequired_types
            if module_item["type"] in unrequired_types or "content_id" in module_item:
                kwargs["module_item"] = module_item
            else:
                raise RequiredFieldMissing(
                    "Dictionary with key 'content_id' is required."
                )
        else:
            raise RequiredFieldMissing("Dictionary with key 'type' is required.")

        response = self._requester.request(
            "POST",
            "courses/{}/modules/{}/items".format(self.course_id, self.id),
            _kwargs=combine_kwargs(**kwargs),
        )
        module_item_json = response.json()
        module_item_json.update({"course_id": self.course_id})

        return ModuleItem(self._requester, module_item_json)


class ModuleItem(CanvasObject):
    def __str__(self):
        return "{} ({})".format(self.title, self.id)

    def edit(self, **kwargs):
        """
        Update this module item.

        :calls: `PUT /api/v1/courses/:course_id/modules/:module_id/items/:id \
        <https://canvas.instructure.com/doc/api/modules.html#method.context_module_items_api.update>`_

        :returns: The updated module item.
        :rtype: :class:`canvasapi.module.ModuleItem`
        """
        response = self._requester.request(
            "PUT",
            "courses/{}/modules/{}/items/{}".format(
                self.course_id, self.module_id, self.id
            ),
            _kwargs=combine_kwargs(**kwargs),
        )
        module_item_json = response.json()
        module_item_json.update({"course_id": self.course_id})

        return ModuleItem(self._requester, module_item_json)

    def delete(self):
        """
        Delete this module item.

        :calls: `DELETE /api/v1/courses/:course_id/modules/:module_id/items/:id \
        <https://canvas.instructure.com/doc/api/modules.html#method.context_module_items_api.destroy>`_

        :rtype: :class:`canvasapi.module.ModuleItem`
        """
        response = self._requester.request(
            "DELETE",
            "courses/{}/modules/{}/items/{}".format(
                self.course_id, self.module_id, self.id
            ),
        )
        module_item_json = response.json()
        module_item_json.update({"course_id": self.course_id})

        return ModuleItem(self._requester, module_item_json)

    def complete(self):
        """
        Mark this module item as done.

        :calls: `PUT /api/v1/courses/:course_id/modules/:module_id/items/:id/done \
        <https://canvas.instructure.com/doc/api/modules.html#method.context_module_items_api.mark_as_done>`_

        :rtype: :class:`canvasapi.module.ModuleItem`
        """
        response = self._requester.request(
            "PUT",
            "courses/{}/modules/{}/items/{}/done".format(
                self.course_id, self.module_id, self.id
            ),
        )
        module_item_json = response.json()
        module_item_json.update({"course_id": self.course_id})

        return ModuleItem(self._requester, module_item_json)

    def uncomplete(self):
        """
        Mark this module item as not done.

        :calls: `DELETE /api/v1/courses/:course_id/modules/:module_id/items/:id/done \
        <https://canvas.instructure.com/doc/api/modules.html#method.context_module_items_api.mark_as_done>`_

        :rtype: :class:`canvasapi.module.ModuleItem`
        """
        response = self._requester.request(
            "DELETE",
            "courses/{}/modules/{}/items/{}/done".format(
                self.course_id, self.module_id, self.id
            ),
        )
        module_item_json = response.json()
        module_item_json.update({"course_id": self.course_id})

        return ModuleItem(self._requester, module_item_json)
