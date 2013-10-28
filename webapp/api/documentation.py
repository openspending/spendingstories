STORY_ENDPOINT =     """
    ## Attributes
    <style>
        table {
            width:100%; 
            text-align:left;
            margin-bottom: 20px;
        }
        tr { 
            min-height: 40px;
            border-bottom: 1px solid #CCC;
        }
        tr:last-child {
            border-bottom: none;
        }
        td, th {
            padding-top: 7px;
            padding-bottom: 7px;
        }
        th {
            min-width: 80px;
        }
    </style>
    <table>
        <thead>
            <tr>
                <th>Name</th>
                <th>Type</th>
                <th>Description</th>
                <th>Example</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Value</td>
                <td>
                    `Float`
                </td>
                <td>
                    The spending amount
                </td>
                <td>
                    `10e6`
                </td>
            </tr>
        </tbody>
    </table>

    
    ## Filter fields 
    Results can be filtered using the following fields:
    <table>
        <thead>
            <tr>
                <th>Name</th>
                <th>Type</th>
                <th>Description</th>
                <th>Possible values</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>
                    **sticky**
                </td>
                <td>
                    `Boolean`
                </td>
                <td> 
                    Will filter stories based on their 
                    `sticky` 
                    attribute.
                </td>
                <td>
                    `True`,
                    `False`,
                    `''`
                </td>
            </tr>
            <tr>
                <td>
                    **country**
                </td>
                <td>
                    `String`
                </td>
                <td> 
                    Will filter stories based on the given country
                </td>
                <td>
                    The iso code of the wanted country, see [/api/countries/](/api/countries/) for more details.
                </td>
            </tr>
            <tr>
                <td>
                    **currency**
                </td>
                <td>
                    `String`
                </td>
                <td>        
                    Will filter stories based on the given currency
                </td>
                <td>
                    The iso code of the wanted currency, see [/api/currencies/](/api/currencies/) for more details.
                </td>
            </tr>
            <tr>
                <td>
                    **type**
                </td>
                <td>
                    `String`
                </td>
                <td>Will filter stories based on their type.</td>
                <td>
                    `over_one_year`, `discrete`, see [the wiki page](/api/currencies/) for more details.
                </td>
            </tr>
            <tr>
                <td>
                    **title**
                </td>
                <td>
                    `String`
                </td>
                <td>Will filter stories based on their title.</td>
                <td>
                    Title of an existing story
                </td>
            </tr>
            <tr>
                <td>
                    **themes**
                </td>
                <td>
                    `String`
                </td>
                <td>
                    Will filter stories based on their theme(s).<br/><br/>
                    **Note:** this attribute is stackable. This means you can add multiple times the same attribute to the URL.<br/>
                    `GET /api/stories/?themes=aid&themes=health` will return all stories having `aid` **OR** `health` in their themes *
                </td>
                <td>
                </td>
            </tr>
        </tbody>
    </table>
    """