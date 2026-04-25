<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <xsl:output method="html" indent="yes" encoding="UTF-8"/>

    <xsl:key name="station-by-id" match="station" use="@id"/>

    <xsl:template match="/">
        <html lang="en">
            <head>
                <meta charset="UTF-8"/>
                <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
                <title>Railway Trips - XML Transformation</title>
                <style>
                    body {
                        margin: 0;
                        font-family: Georgia, "Times New Roman", serif;
                        color: #201a17;
                        background:
                            radial-gradient(circle at top left, rgba(201, 111, 58, 0.18), transparent 24%),
                            radial-gradient(circle at top right, rgba(13, 107, 93, 0.18), transparent 24%),
                            linear-gradient(180deg, #fbf4ea 0%, #f6efe5 100%);
                    }

                    .page {
                        width: min(1180px, calc(100% - 2rem));
                        margin: 0 auto;
                        padding: 2rem 0 3rem;
                    }

                    .hero {
                        text-align: center;
                        padding: 1rem 0 2rem;
                    }

                    .eyebrow {
                        color: #c96f3a;
                        text-transform: uppercase;
                        letter-spacing: 0.18em;
                        font-weight: bold;
                        font-size: 0.85rem;
                    }

                    h1 {
                        font-size: 3rem;
                        margin: 0.4rem 0;
                    }

                    .hero p {
                        color: #665b54;
                        max-width: 720px;
                        margin: 0 auto;
                    }

                    .line-card {
                        background: #fffaf4;
                        border: 1px solid #ddcfbf;
                        border-radius: 24px;
                        padding: 1.25rem;
                        margin-bottom: 1rem;
                        box-shadow: 0 18px 40px rgba(58, 39, 26, 0.12);
                    }

                    .line-title {
                        font-size: 1.35rem;
                        margin: 0 0 1rem;
                    }

                    .trip-grid {
                        display: grid;
                        grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
                        gap: 1rem;
                    }

                    .trip-card {
                        border: 1px solid #e6d9cc;
                        border-radius: 18px;
                        padding: 1rem;
                        background: white;
                    }

                    .trip-badge {
                        display: inline-block;
                        padding: 0.3rem 0.65rem;
                        border-radius: 999px;
                        background: #e3f1ed;
                        color: #08473f;
                        font-weight: bold;
                        font-size: 0.9rem;
                    }

                    .classes span {
                        display: inline-block;
                        margin: 0.2rem 0.35rem 0.2rem 0;
                        padding: 0.3rem 0.6rem;
                        border-radius: 999px;
                        background: #efe3d4;
                    }

                    strong {
                        color: #08473f;
                    }
                </style>
            </head>
            <body>
                <div class="page">
                    <section class="hero">
                        <p class="eyebrow">Part 1 - XSLT Transformation</p>
                        <h1>Railway Trip Management</h1>
                        <p>
                            This HTML page is generated directly from <code>transport.xml</code>
                            using <code>trains.xsl</code>.
                        </p>
                    </section>

                    <xsl:for-each select="transport/lines/line">
                        <div class="line-card">
                            <h2 class="line-title">
                                Line <xsl:value-of select="@code"/>:
                                <xsl:value-of select="key('station-by-id', @departure)/@name"/>
                                &#8594;
                                <xsl:value-of select="key('station-by-id', @arrival)/@name"/>
                            </h2>

                            <div class="trip-grid">
                                <xsl:for-each select="trips/trip">
                                    <div class="trip-card">
                                        <p class="trip-badge">
                                            Trip <xsl:value-of select="@code"/>
                                        </p>
                                        <p><strong>Train type:</strong> <xsl:value-of select="@type"/></p>
                                        <p>
                                            <strong>Schedule:</strong>
                                            <xsl:value-of select="schedule/@departure"/>
                                            -
                                            <xsl:value-of select="schedule/@arrival"/>
                                        </p>
                                        <p><strong>Days:</strong> <xsl:value-of select="days"/></p>
                                        <div class="classes">
                                            <strong>Classes:</strong>
                                            <xsl:text> </xsl:text>
                                            <xsl:for-each select="class">
                                                <span>
                                                    <xsl:value-of select="@type"/>:
                                                    <xsl:value-of select="@price"/> DZD
                                                </span>
                                            </xsl:for-each>
                                        </div>
                                    </div>
                                </xsl:for-each>
                            </div>
                        </div>
                    </xsl:for-each>
                </div>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>
