<xsl:transform xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

    <xsl:template name="lang-dropdown">
        <button class="dropbtn" onclick="dropDown()">Dropdown
            <i class="fa fa-caret-down"></i>
        </button>
        <div class="dropdown-content" id="lang-dropdown">
            <a href="#" id="spa">Link 1</a>
            <a href="#" id="kor">Link 2</a>
            <a href="#" id="zho1">Link 3</a>
        </div>
    </xsl:template>

</xsl:transform>