import warnings

from canvasapi.canvas_object import CanvasObject
from canvasapi.paginated_list import PaginatedList
from canvasapi.util import combine_kwargs, obj_or_id


class EPortfolio(CanvasObject):
    def __str__(self):
        return "{}".format(self.name)

    # TODO: Write test
    def delete(self):
        """
        Delete an ePortfolio.

        :calls: `DELETE /api/v1/eportfolios/:id`_ \
            `<https://canvas.instructure.com/doc/api/e_portfolios.html#method.eportfolios_api.delete>`
        
        :returns: ePortfolio with deleted date set.
        :rtype: `canvasapi.eportfolio.EPortfolio`
        """
        response = self._requester.request("DELETE", "eportfolios/{}".format(self.id))
        return EPortfolio(self._requester, response.json())

    # TODO: Add test
    def get_eportfolio(self, eportfolio, **kwargs):
        """
        Get an eportfolio by ID.

        :param eportfolio: The object or ID of the eportfolio to retrieve.
        :type eportfolio: :class: `canvasapi.eportfolio.EPortfolio` or int

        :calls: `GET /api/v1/eportfolios/:id` \
            `<https://canvas.instructure.com/doc/api/e_portfolios.html#method.eportfolios_api.show>`_

        :rtype: :class:`canvasapi.eportfolio.EPortfolio`
        """
        eportfolio_id = obj_or_id(eportfolio, "eportfolio", (EPortfolio,))
        response = self._requester.request(
            "GET",
            "eportfolios/{}".format(eportfolio_id),
            _kwargs=combine_kwargs(**kwargs),
        )

        return EPortfolio(self._requester, response.json())

    # TODO: Write test
    def get_eportfolio_pages(self, eportfolio, **kwargs):
        """ 
        Return a list of pages for an ePortfolio.

        :param eportfolio: The object or ID of the ePortfolio to retrieve.
        :type eportfolio: :class: `canvasapi.eportfolio.EPortfolio` or int

        :calls: `GET /api/v1/eportfolios/:eportfolio_id/pages` \
            `<https://canvas.instructure.com/doc/api/e_portfolios.html#method.eportfolios_api.pages>`_

        :returns: List of ePortfolio pages.
        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.eportfolio.EPortfolioPage`
        """
        eportfolio_id = obj_or_id(eportfolio, "eportfolio", (EPortfolio,))

        return PaginatedList(
            EPortfolioPage,
            self._requester,
            "GET",
            "eportfolios/{}/pages".format(eportfolio_id),
            _kwargs=combine_kwargs(**kwargs),
        )

    # TODO: Write test
    def moderate_eportfolio(self, eportfolio, **kwargs):
        """
        Update the spam_status of an eportfolio. Only available to admins who can `moderate_user_content`.

        :param eportfolio: The object or ID of the ePortfolio to retrieve.
        :type eportfolio: :class: `canvasapi.eportfolio.EPortfolio` or int

        :calls: `PUT /api/v1/eportfolios/:eportfolio_id/moderate` \
            `<https://canvas.instructure.com/doc/api/e_portfolios.html#method.eportfolios_api.moderate>`_

        :returns: Updated ePortfolio.
        :rtype: :class:`canvasapi.eportfolio.EPortfolio`
        """
        eportfolio_id = obj_or_id(eportfolio, "eportfolio", (EPortfolio,))
        response = self._requester.request(
            "PUT", "eportfolios/{}/moderate", _kwargs=combine_kwargs(**kwargs)
        )

        return EPortfolio(self._requester, response.json())

    # TODO: Write test
    def restore_deleted_eportfolio(self, eportfolio, **kwargs):
        """
        Restore an ePortfolio back to active that was previously deleted. Only available to admins who can moderate_user_content.

        :param eportfolio: The object or ID of the ePortfolio to retrieve.
        :type eportfolio: :class: `canvasapi.eportfolio.EPortfolio` or int

        :calls: `PUT /api/v1/eportfolios/:eportfolio_id/restore` \
            `<https://canvas.instructure.com/doc/api/e_portfolios.html#method.eportfolios_api.restore>`_

       :returns: Updated ePortfolio.
       :rtype: :class: `canvasapi.eportfolio.EPortfolio`
        """
        eportfolio_id = obj_or_id(eportfolio, "eportfolio", (EPortfolio,))
        response = self._requester.request(
            "PUT",
            "eportfolios/{}/restore".format(eportfolio_id),
            _kwargs=combine_kwargs(**kwargs),
        )

        return EPortfolio(self._requester, response.json())


class EPortfolioPage(CanvasObject):
    def __str__(self):
        return "{}. {}".format(self.position, self.name)
