<xsl:transform xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
   <xsl:include href="navigation.xslt"/>
   <xsl:output method="html"/>

   <xsl:template match="navbar">
        <call:template name="navbar"/>
   </xsl:template>
</xsl:transform>