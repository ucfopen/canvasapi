from canvas_object import CanvasObject
from exceptions import RequiredFieldMissing
from paginated_list import PaginatedList
from util import combine_kwargs


class Module(CanvasObject):

    def __str__(self):
        return "id: %s, name: %s" % (
            self.id,
            self.name,
        )

    def edit(self, course_id, **kwargs):
        """
        Update this module.

        :calls: `PUT /api/v1/courses/:course_id/modules/:id \
        <https://canvas.instructure.com/doc/api/modules.html#method.context_modules_api.update>`_

        :rtype: :class:`pycanvas.module.Module`
        """
        response = self._requester.request(
            'PUT',
            'courses/%s/modules/%s' % (course_id, self.id),
            **kwargs
        )
        return Module(self._requester, response.json())

    def delete(self, course_id):
        """
        Delete this module.

        :calls: `DELETE /api/v1/courses/:course_id/modules/:id \
        <https://canvas.instructure.com/doc/api/modules.html#method.context_modules_api.destroy>`_

        :rtype: :class:`pycanvas.module.Module`
        """
        response = self._requester.request(
            'DELETE',
            'courses/%s/modules/%s' % (course_id, self.id),
        )
        return Module(self._requester, response.json())

    def relock(self, course_id):
        """
        Reset module progressions to their default locked state and recalculates
        them based on the current requirements.

        Adding progression requirements to an active course will not lock students
        out of modules they have already unlocked unless this action is called.

        :calls: `PUT /api/v1/courses/:course_id/modules/:id/relock \
        <https://canvas.instructure.com/doc/api/modules.html#method.context_modules_api.relock>`_

        :rtype: :class:`pycanvas.module.Module`
        """
        response = self._requester.request(
            'PUT',
            'courses/%s/modules/%s/relock' % (course_id, self.id),
        )
        return Module(self._requester, response.json())

    def list_module_items(self, course_id):
        """
        List all of the items in this module.

        :calls: `GET /api/v1/courses/:course_id/modules/:module_id/items \
        <https://canvas.instructure.com/doc/api/modules.html#method.context_module_items_api.index>`_

        :rtype: :class:`pycanvas.paginated_list.PaginatedList` of :class:`pycanvas.module.ModuleItem`
        """
        return PaginatedList(
            ModuleItem,
            self._requester,
            'GET',
            'courses/%s/modules/%s/items' % (course_id, self.id)
        )

    def get_module_item(self, course_id, module_item_id):
        """
        Retrieve a module item by ID.

        :calls: `GET /api/v1/courses/:course_id/modules/:module_id/items/:id \
        <https://canvas.instructure.com/doc/api/modules.html#method.context_module_items_api.show>`_

        :rtype: :class:`pycanvas.module.ModuleItem`
        """
        response = self._requester.request(
            'GET',
            'courses/%s/modules/%s/items/%s' % (course_id, self.id, module_item_id)
        )
        return ModuleItem(self._requester, response.json())

    def create_module_item(self, course_id, module_item, **kwargs):
        """
        Create a module item.

        :calls: `POST /api/v1/courses/:course_id/modules/:module_id/items \
        <https://canvas.instructure.com/doc/api/modules.html#method.context_module_items_api.create>`_

        :param module_item: The attributes to create the module item with.
        :type module_item: dict
        :returns: The created module item.
        :rtype: :class:`pycanvas.module.ModuleItem`
        """
        if isinstance(module_item, dict) and 'type' in module_item:
            if 'content_id' in module_item:
                kwargs['module_item'] = module_item
            else:
                raise RequiredFieldMissing("Dictionary with key 'content_id' is required.")
        else:
            raise RequiredFieldMissing("Dictionary with key 'type' is required.")

        response = self._requester.request(
            'POST',
            'courses/%s/modules/%s/items' % (course_id, self.id),
            **combine_kwargs(**kwargs)
        )

        return ModuleItem(self._requester, response.json())


class ModuleItem(CanvasObject):

    def __str__(self):
        return "id: %s, title: %s, description: %s" % (
            self.id,
            self.title,
            self.module_id
        )

    def edit(self, course_id, **kwargs):
        """
        Update this module item.

        :calls: `PUT /api/v1/courses/:course_id/modules/:id \
        <https://canvas.instructure.com/doc/api/modules.html#method.context_modules_api.update>`_

        :returns: The updated module item.
        :rtype: :class:`pycanvas.module.ModuleItem`
        """
        response = self._requester.request(
            'PUT',
            'courses/%s/modules/%s/items/%s' % (course_id, self.module_id, self.id),
            **kwargs
        )
        return ModuleItem(self._requester, response.json())

    def delete(self, course_id):
        """
        Delete this module item.

        :calls: `DELETE /api/v1/courses/:course_id/modules/:module_id/items/:id \
        <https://canvas.instructure.com/doc/api/modules.html#method.context_module_items_api.destroy>`_

        :rtype: :class:`pycanvas.module.ModuleItem`
        """
        response = self._requester.request(
            'DELETE',
            'courses/%s/modules/%s/items/%s' % (course_id, self.module_id, self.id),
        )
        return ModuleItem(self._requester, response.json())

    def complete(self, course_id):
        """
        Mark this module item as done.

        :calls: `PUT /api/v1/courses/:course_id/modules/:module_id/items/:id/done \
        <https://canvas.instructure.com/doc/api/modules.html#method.context_module_items_api.mark_as_done>`_

        :rtype: :class:`pycanvas.module.ModuleItem`
        """
        response = self._requester.request(
            'PUT',
            'courses/%s/modules/%s/items/%s/done' % (course_id, self.module_id, self.id),
        )
        return ModuleItem(self._requester, response.json())

    def uncomplete(self, course_id):
        """
        Mark this module item as not done.

        :calls: `DELETE /api/v1/courses/:course_id/modules/:module_id/items/:id/done \
        <https://canvas.instructure.com/doc/api/modules.html#method.context_module_items_api.mark_as_done>`_

        :rtype: :class:`pycanvas.module.ModuleItem`
        """
        response = self._requester.request(
            'DELETE',
            'courses/%s/modules/%s/items/%s/done' % (course_id, self.module_id, self.id),
        )
        return ModuleItem(self._requester, response.json())
