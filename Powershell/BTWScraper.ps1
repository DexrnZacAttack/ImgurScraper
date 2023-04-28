mkdir C:\TEMP
Invoke-WebRequest -Uri 'https://www.nuget.org/api/v2/package/HtmlAgilityPack/' -OutFile 'C:\TEMP\HtmlAgilityPack.nupkg'
ren C:\TEMP\HtmlAgilityPack.nupkg HtmlAgilityPack.zip 
Expand-Archive -Path 'C:\TEMP\HtmlAgilityPack.zip' -DestinationPath 'C:\TEMP\HtmlAgilityPack'
Import-Module C:\TEMP\HtmlAgilityPack\lib\net40\HtmlAgilityPack.dll

cls
Add-Type -AssemblyName System.Web
Add-Type -Path "HtmlAgilityPack.dll"

# set the base URL of the forum
$base_url = "https://sargunster.com/btwforum/viewtopic.php?t="

$headers = @{
    "User-Agent" = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
}

# set the starting topic ID to crawl
$start_topic_id = 10000

# set the ending topic ID to crawl
$end_topic_id = 100000

# create a file to store the links (if it doesn't exist)
$links_file = "links.txt"
if (!(Test-Path $links_file)) {
    New-Item $links_file -ItemType File | Out-Null
}

function Crawl-Topics($start_topic_id, $end_topic_id) {
    $client = New-Object System.Net.WebClient
    for ($topic_id = $start_topic_id; $topic_id -le $end_topic_id; $topic_id++) {
        # create a full URL by combining the base URL with the topic ID
        $full_url = $base_url + $topic_id

        # make a GET request to the topic page
        $response = $client.DownloadString($full_url)

        # check if the topic exists
        if ($response.Contains("The requested topic does not exist.")) {
            Write-Host "Topic $topic_id does not exist."
        } else {
            # parse the HTML content using HtmlAgilityPack
            $html = New-Object HtmlAgilityPack.HtmlDocument
            $html.LoadHtml($response)

            # find all img tags on the page
            $img_tags = $html.DocumentNode.SelectNodes('//img')
            
            # iterate over the img tags and save any direct image links to the file
            foreach ($img_tag in $img_tags) {
                $src = $img_tag.GetAttributeValue("src", "")
                if ($src -and $src.Contains("imgur") -and ($src.Contains(".jpg") -or $src.Contains(".png") -or $src.Contains(".gif"))) {
                    Write-Host "Found imgur link: $src"
                    # write the link to the file
                    Add-Content $links_file $src
                }
            }

            # print the percentage of topics done
            $percent_done = [int](($topic_id - $start_topic_id + 1) / ($end_topic_id - $start_topic_id + 1) * 100)
            Write-Progress -Activity "Crawling topics" -Status "$percent_done% done" -PercentComplete $percent_done
        }
    }
}

Crawl-Topics $start_topic_id $end_topic_id


#Cleanup

$filePath = 'links.txt'
$fileContent = Get-Content $filePath -Raw

# Use a hashtable to keep track of unique lines
$uniqueLines = @{}

# Keep track of the number of characters written so far
$charCount = 0

# Split the file content into an array of lines
$lines = $fileContent -split "`n"

# Clear the file content
Clear-Content $filePath

foreach ($line in $lines) {
    # Strip any whitespace from the beginning and end of the line
    $line = $line.Trim()

    # Only write the line back to the file if it hasn't already been written
    if ($uniqueLines.ContainsKey($line) -eq $false) {
        # Add the line to the hashtable of unique lines
        $uniqueLines.Add($line, $null)

        # Add the length of the line to the character count
        $charCount += $line.Length

        # Write the line to the file
        Add-Content $filePath $line

        # If we've written 1000 characters or more, add a blank line
        if ($charCount -ge 1000) {
            Add-Content $filePath ""
            
            # Reset the character count
            $charCount = 0
        }
    }
}

# If the last line didn't end in a newline character, add one to ensure the file ends with a newline
if ($lines[-1] -notmatch "`n$") {
    Add-Content $filePath ""
}

# Print the number of unique links
Write-Host "Number of unique links: $($uniqueLines.Count)"
